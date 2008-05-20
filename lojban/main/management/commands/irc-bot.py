
import os, sys, signal, resource
from os.path import join, normpath
from datetime import datetime
from functools import partial

import irclib

from django.core.management.base import BaseCommand
from django.conf import settings

from lojban.main.models import *

nick = "joncku"
name ="Lojban website integration bot"
password = None

pid_filename = normpath(join(settings.LOCAL_PATH, "run", "irc-bot.pid"))
log_filename = normpath(join(settings.LOCAL_PATH, "run", "irc-bot.log"))
working_dir = "/"

irc = irclib.IRC()

users = {}

def start_daemon():
    # It's quite tricky to start a daemon properly.  For more information, read 
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/278731

    # Start a grandchild process.
    pid = os.fork()
    if pid == 0:
        os.setsid()
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        pid = os.fork()
        if pid != 0:
            os._exit(0)
    else:
        os._exit(0)

    os.chdir(working_dir)
    os.umask(0)

    # Save the process id.
    try:
        pid_file = os.open(pid_filename, os.O_WRONLY|os.O_EXCL|os.O_CREAT)
        os.write(pid_file, str(os.getpid()))
        os.close(pid_file)
    except OSError:
        raise SystemExit("Unable to open PID file: is the IRC bot already running?")

    # Close all file descriptors
    max_fd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (max_fd == resource.RLIM_INFINITY):
        max_fd = 1024
    for fd in range(0, max_fd):
        try:
            os.close(fd)
        except OSError:
            pass

    # Direct all input/output to /dev/null
    os.open(os.devnull, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)

def stop_daemon():
    try:
        pid_file = open(pid_filename)
        os.kill(int(pid_file.read()), signal.SIGTERM)
        pid_file.close()
        os.remove(pid_filename)
    except IOError:
        raise SystemExit("Unable to open PID file: is the IRC bot running?")

def handlePublicMessage(channel, connection, event):
    channel.last_activity = datetime.now()
    channel.save()

def handleJoin(channel, connection, event):
    users[event.source().split("!")[0]] = ""
    channel.last_activity = datetime.now()
    channel.headcount = len(users)
    channel.save()

def handlePart(channel, connection, event):
    del users[event.source().split("!")[0]]
    channel.last_activity = datetime.now()
    channel.headcount = len(users)
    channel.save()

def handleNames(channel, connection, event):
    global users
    users.clear()
    for user in event.arguments()[2].split():
        if user[0] == "@" or user[0] == "+":
            users[user[1:]] = ""
        else:
            users[user] = ""
    channel.last_activity = datetime.now()
    channel.headcount = len(users)
    channel.save()

class Command(BaseCommand):

    help = "Controls an IRC bot that monitors a channel for traffic."
    args = "start|stop"

    def handle(self, action=None, **options):

        if action is None or action not in ("start", "stop"):
            print "You need to specify whether you want to start or stop the server."
            return

        if action == "start":
            start_daemon()

            try:
                # We assume only one channel is configured.
                channel = IRCChannel.objects.get()

                irc.add_global_handler("join", partial(handleJoin, channel))
                irc.add_global_handler("part", partial(handlePart, channel))
                irc.add_global_handler("quit", partial(handlePart, channel))
                irc.add_global_handler("kick", partial(handlePart, channel))
                irc.add_global_handler("namreply", partial(handleNames, channel))
                irc.add_global_handler("pubmsg", partial(handlePublicMessage, channel))

                server = irc.server()
                server.connect(channel.server, channel.port, nick, ircname=name)
                if password is not None:
                    server.privmsg("NickServ", "identify %s" % password)
                server.join(channel.name)

                irc.process_forever()
            except Exception, e:
                log_file = open(log_filename, "ab")
                log_file.write(str(e) + "\n")
                log_file.close()
            finally:
                stop_daemon()

        elif action == "stop":
            stop_daemon()



