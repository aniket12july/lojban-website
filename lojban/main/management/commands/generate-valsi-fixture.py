
import sys, os
from os.path import join, dirname, normpath, exists
from os import mkdir, pardir
from urllib import urlretrieve
from xml.etree.cElementTree import iterparse, ElementTree, Element

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        base_dir = normpath(join(dirname(__file__), pardir, pardir, pardir, pardir))
        data_dir = join(base_dir, 'data')
        fixture_dir = join(base_dir, 'lojban/main/fixtures')
        valsi_file = join(data_dir, 'valsi.xml')
        valsi_uri = 'http://jbovlaste.lojban.org/export/xml-export.html?lang=en'

        sys.path.append(base_dir)

        os.environ['DJANGO_SETTINGS_MODULE'] = 'lojban.settings'

        if not exists(data_dir):
            mkdir(data_dir)

        if not exists(valsi_file):
            print "The valsi file is not available locally, so it will be downloaded.  This may take a while..."
            def report(count, size, total):
                accuracy = ""
                if total == -1:
                    # Filesize is around 1MB.
                    total = 1024**2
                    accuracy = "(approx.)"
                progress = float(count*size)/total
                if progress > 1:
                    progress = 1
                print "\r%d%% complete %s." % (progress*100, accuracy),
                sys.stdout.flush()
            urlretrieve(valsi_uri, valsi_file, report)
            print "\rThe valsi file has been downloaded."

        if not exists(fixture_dir):
            mkdir(fixture_dir)

        fixture = ElementTree(Element("django-objects"))
        fixture_root = fixture.getroot()
        fixture_root.attrib["version"] = "1.0"

        parser = iterparse(valsi_file, events=("start", "end"))
        parser = iter(parser)
        event, root = parser.next()
        keys = {}
        selmaho = {}
        for event, element in parser:
            if event != "end":
                root.clear()
                continue
            if element.tag != "valsi":
                root.clear()
                continue

            if element.attrib["type"] == "gismu" or element.attrib["type"] == "experimental gismu":
                valsi_type = "gismu"
            elif element.attrib["type"] == "cmavo" or element.attrib["type"] == "experimental cmavo":
                valsi_type = "cmavo"
            elif element.attrib["type"] == "cmavo cluster":
                root.clear()
                continue
            elif element.attrib["type"] == "cmene":
                root.clear()
                continue
            elif element.attrib["type"] == "fu'ivla":
                valsi_type = "fuhivla"
            elif element.attrib["type"] == "lujvo":
                valsi_type = "lujvo"
            else:
                raise Exception("Unrecognised type of valsi found: '%s'." % element.attrib["type"])

            valsi = Element("object")
            keys[valsi_type] = keys.get(valsi_type, 0) + 1
            valsi.attrib["pk"] = str(keys[valsi_type])
            valsi.attrib["model"] = "main." + valsi_type

            name = Element("field")
            name.attrib["type"] = "CharField"
            name.attrib["name"] = "name"
            name.text = element.attrib["word"]
            valsi.append(name)

            definition = Element("field")
            definition.attrib["type"] = "TextField"
            definition.attrib["name"] = "definition"
            definition.text = element.findtext("definition")
            valsi.append(definition)

            notes_text = element.findtext("notes")
            if notes_text is not None:
                notes = Element("field")
                notes.attrib["type"] = "TextField"
                notes.attrib["name"] = "notes"
                notes.text = notes_text
                valsi.append(notes)

            if element.attrib.get("unofficial", "false") == "true":
                official = Element("field")
                official.attrib["type"] = "BooleanField"
                official.attrib["name"] = "official"
                official.text = "False"
                valsi.append(official)

            if valsi_type == "gismu":
                for rafsi in element.findall("rafsi"):
                    new_rafsi = Element("field")
                    new_rafsi.attrib["type"] = "CharField"
                    if len(rafsi.text) == 4:
                        new_rafsi.attrib["name"] = "cvv_rafsi"
                    elif rafsi.text[1:2] in "aeiou":
                        new_rafsi.attrib["name"] = "cvc_rafsi"
                    else:
                        new_rafsi.attrib["name"] = "ccv_rafsi"
                    new_rafsi.text = rafsi.text
                    valsi.append(new_rafsi)

            if valsi_type == "cmavo":
                cmavo_selmaho = element.findtext("selmaho")
                if cmavo_selmaho not in selmaho:
                    selmaho[cmavo_selmaho] = len(selmaho) + 1
                    selmaho_element = Element("object")
                    selmaho_element.attrib["pk"] = str(len(selmaho))
                    selmaho_element.attrib["model"] = "main.selmaho"

                    name = Element("field")
                    name.attrib["type"] = "CharField"
                    name.attrib["name"] = "name"
                    name.text = cmavo_selmaho or "Unknown"

                    selmaho_element.append(name)
                    fixture_root.append(selmaho_element)
                selmaho_ref = Element("field")
                selmaho_ref.attrib["to"] = "main.selmaho"
                selmaho_ref.attrib["name"] = "selmaho"
                selmaho_ref.attrib["rel"] = "ManyToOneRel"
                selmaho_ref.text = str(selmaho[cmavo_selmaho])
                valsi.append(selmaho_ref)

            fixture_root.append(valsi)
            root.clear()

        fixture.write(join(fixture_dir, "valsi.xml"))

