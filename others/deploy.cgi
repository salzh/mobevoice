#!/usr/bin/python
#__author__ = 'Pheonix'


print "Content-type: text/html"
print
print "Hi"
exit()
import pickle
import cgi
import os
from fabric.api import *

#env.hosts = ['parth@zenofon.com:2322']
env.host_string = 'localhost'
#
#run("ls ~")
#exit()
class svn:
    def __init__(self, url, deployBase):
        self.url = url
        self.base = "svn %%s %s --username=parth --password=parthtemp --non-interactive --trust-server-cert %%s" % (url)
        self.revisions = {}
        self.deployBase = deployBase

    def getRevisionList(self, force = 0):
        if not force:
            try:
                file = open("./svn_log", "r")
                self.revisions = pickle.load(file)
                return self.revisions
            except:
                pass


        revMap = {}
        data = os.popen (self.base % ("log", "")).read()
        data = data.split("\n")
        count = len(data)
        for i in range(count):
            line = data[i]
            if not line.split("|").__len__() > 2:
                continue

            rev = int(line.split("|")[0].strip()[1:])
#            print "revision : " + str(rev)

            i+=1
            desc = ""
            while data[i] != "------------------------------------------------------------------------":
                desc += data[i] + "\n"
                i+=1

            desc = desc.strip()

            revMap[rev] = desc

        self.revisions = revMap
        file = open("./svn_log", "w+")
        pickle.dump(revMap, file)
        file.close()
        return revMap

    def getRevisions(self):
        if self.revisions.__len__() < 2:
            return self.getRevisionList()
        else:
            return self.revisions

    def getChangedFiles(self, rev, force = 0):
        print "Getting file Changes: %s" % rev
        path = "./revisions/%s.log" % rev
        if not force:
            try:
                file = open(path, "r")
                return pickle.load(file)
            except:
                pass

        command =  self.base % ("diff --summarize", "-r " + str(rev))
        data = os.popen(command).read()
        data = data.split("\n")
        files = []
        for i in range(len(data)):
            line = data[i]
            if line[:1] == "M" or line[:1] == "A":
                files.append(line.split(self.url)[1])

        file = open(path, "w+")
        pickle.dump(files, file)
        print files
        return data

    def deployRevision(self, rev):
        time = os.popen("date +%s").read().split("\n")[0]
        dirPath ="./move_backup/%s_%s/" % (time, rev)
        old = dirPath + "old/"
        new = "./temp/"
        os.mkdir(dirPath)
        os.mkdir(old)
        os.popen("rm -rf %s" % new)
        os.mkdir(new)
        files = self.getChangedFiles(rev)
        for file in files:
            print "Copying File %s to %s" % (file, old)
#            print "cp %s %s" % (self.deployBase + file, old)
            os.popen("cp %s %s" % (self.deployBase + file, old)).read()

        local("cd " + new)
        exportCommand = "cd %s && svn export %s/%%s --username=parth --password=parthtemp --non-interactive --trust-server-cert -r %s" % (new, self.url, rev)
        print "\n\n"
        for file in files:
            print "Exporting File from SVN : %s" % file
#            print exportCommand % file
            local(exportCommand % file)

        for file in files:
            os.popen("echo parth123 | sudo -S cp %s %s" % (new + file, self.deployBase + file))
            os.popen("echo parth123 | sudo -S chmod +x %s " % (self.deployBase + file))

    def revertMove(self, move):
        rev = move.split("_")[1]
        files = self.getChangedFiles(rev)
        old = "./move_backup/%s/old/" % move
        for file in files:
            os.popen("echo parth123 | sudo -S cp %s %s" % (old + file, self.deployBase + file))




zenofon = svn("https://dev.zenofon.com/svn/zenofon/trunk/", "/usr/local/multilevel/")

params = cgi.FieldStorage()

print "Content-type: text/html\n\n"
print params


#print zenofon.getRevisions()
#print zenofon.deployRevision(431)
