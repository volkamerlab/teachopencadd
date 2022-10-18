#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright 2012-2022 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Python Client Automatically generated with:
# https://github.com/ebi-wp/webservice-clients-generator
#
# Clustal Omega (REST) web service Python client using xmltramp2.
#
# For further information see:
# https://www.ebi.ac.uk/Tools/webservices/
#
###############################################################################

from __future__ import print_function

import os
import sys
import time
import requests
import platform
from xmltramp2 import xmltramp
from optparse import OptionParser

try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
    from urllib.request import __version__ as urllib_version
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError
    from urllib2 import __version__ as urllib_version

# allow unicode(str) to be used in python 3
try:
    unicode('')
except NameError:
    unicode = str

# Base URL for service
baseUrl = u'https://www.ebi.ac.uk/Tools/services/rest/clustalo'
version = u'2022-09-13 12:15'

# Set interval for checking status
pollFreq = 3
# Output level
outputLevel = 1
# Debug level
debugLevel = 0
# Number of option arguments.
numOpts = len(sys.argv)

# Process command-line options
parser = OptionParser(add_help_option=False)

# Tool specific options (Try to print all the commands automatically)
parser.add_option('--guidetreeout', action='store_true', help=('Output guide tree.'))
parser.add_option('--addformats', action='store_true', help=('Output additional output formats'))
parser.add_option('--dismatout', action='store_true', help=('Output distance matrix. This is only calculated if the mBed-like'
                  'clustering guide tree is set to false.'))
parser.add_option('--dealign', action='store_true', help=('Remove any existing alignment (gaps) from input sequences.'))
parser.add_option('--mbed', action='store_true', help=('This option uses a sample of the input sequences and then represents'
                  'all sequences as vectors to these sequences, enabling much more rapid'
                  'generation of the guide tree, especially when the number of sequences'
                  'is large.'))
parser.add_option('--mbediteration', action='store_true', help=('Use mBed-like clustering during subsequent iterations.'))
parser.add_option('--iterations', type=int, help=('Number of (combined guide-tree/HMM) iterations.'))
parser.add_option('--gtiterations', type=int, help=('Having set the number of combined iterations, this parameter can be'
                  'changed to limit the number of guide tree iterations within the'
                  'combined iterations.'))
parser.add_option('--hmmiterations', type=int, help=('Having set the number of combined iterations, this parameter can be'
                  'changed to limit the number of HMM iterations within the combined'
                  'iterations.'))
parser.add_option('--outfmt', type=str, help=('Format for generated multiple sequence alignment.'))
parser.add_option('--order', type=str, help=('The order in which the sequences appear in the final alignment'))
parser.add_option('--stype', type=str, help=('Defines the type of the sequences to be aligned'))
parser.add_option('--sequence', type=str, help=('Three or more sequences to be aligned can be entered directly into'
                  'this box. Sequences can be in GCG, FASTA, EMBL (Nucleotide only),'
                  'GenBank, PIR, NBRF, PHYLIP or UniProtKB/Swiss-Prot (Protein only)'
                  'format. Partially formatted sequences are not accepted. Adding a'
                  'return to the end of the sequence may help certain applications'
                  'understand the input. Note that directly using data from word'
                  'processors may yield unpredictable results as hidden/control'
                  'characters may be present. There is currently a sequence input limit'
                  'of 4000 sequences and 4MB of data.'))
# General options
parser.add_option('-h', '--help', action='store_true', help='Show this help message and exit.')
parser.add_option('--email', help='E-mail address.')
parser.add_option('--title', help='Job title.')
parser.add_option('--outfile', help='File name for results.')
parser.add_option('--outformat', help='Output format for results.')
parser.add_option('--asyncjob', action='store_true', help='Asynchronous mode.')
parser.add_option('--jobid', help='Job identifier.')
parser.add_option('--polljob', action="store_true", help='Get job result.')
parser.add_option('--pollFreq', type='int', default=3, help='Poll frequency in seconds (default 3s).')
parser.add_option('--status', action="store_true", help='Get job status.')
parser.add_option('--resultTypes', action='store_true', help='Get result types.')
parser.add_option('--params', action='store_true', help='List input parameters.')
parser.add_option('--paramDetail', help='Get details for parameter.')
parser.add_option('--quiet', action='store_true', help='Decrease output level.')
parser.add_option('--verbose', action='store_true', help='Increase output level.')
parser.add_option('--version', action='store_true', help='Prints out the version of the Client and exit.')
parser.add_option('--debugLevel', type='int', default=debugLevel, help='Debugging level.')
parser.add_option('--baseUrl', default=baseUrl, help='Base URL for service.')

(options, args) = parser.parse_args()

# Increase output level
if options.verbose:
    outputLevel += 1

# Decrease output level
if options.quiet:
    outputLevel -= 1

# Debug level
if options.debugLevel:
    debugLevel = options.debugLevel

if options.pollFreq:
    pollFreq = options.pollFreq

if options.baseUrl:
    baseUrl = options.baseUrl


# Debug print
def printDebugMessage(functionName, message, level):
    if (level <= debugLevel):
        print(u'[' + functionName + u'] ' + message, file=sys.stderr)


# User-agent for request (see RFC2616).
def getUserAgent():
    printDebugMessage(u'getUserAgent', u'Begin', 11)
    # Agent string for urllib2 library.
    urllib_agent = u'Python-urllib/%s' % urllib_version
    clientRevision = version
    # Prepend client specific agent string.
    try:
        pythonversion = platform.python_version()
        pythonsys = platform.system()
    except ValueError:
        pythonversion, pythonsys = "Unknown", "Unknown"
    user_agent = u'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
        clientRevision, os.path.basename(__file__),
        pythonversion, pythonsys, urllib_agent)
    printDebugMessage(u'getUserAgent', u'user_agent: ' + user_agent, 12)
    printDebugMessage(u'getUserAgent', u'End', 11)
    return user_agent


# Wrapper for a REST (HTTP GET) request
def restRequest(url):
    printDebugMessage(u'restRequest', u'Begin', 11)
    printDebugMessage(u'restRequest', u'url: ' + url, 11)
    try:
        # Set the User-agent.
        user_agent = getUserAgent()
        http_headers = {u'User-Agent': user_agent}
        req = Request(url, None, http_headers)
        # Make the request (HTTP GET).
        reqH = urlopen(req)
        resp = reqH.read()
        contenttype = reqH.info()

        if (len(resp) > 0 and contenttype != u"image/png;charset=UTF-8"
                and contenttype != u"image/jpeg;charset=UTF-8"
                and contenttype != u"application/gzip;charset=UTF-8"):
            try:
                result = unicode(resp, u'utf-8')
            except UnicodeDecodeError:
                result = resp
        else:
            result = resp
        reqH.close()
    # Errors are indicated by HTTP status codes.
    except HTTPError as ex:
        result = requests.get(url).content
    printDebugMessage(u'restRequest', u'End', 11)
    return result


# Get input parameters list
def serviceGetParameters():
    printDebugMessage(u'serviceGetParameters', u'Begin', 1)
    requestUrl = baseUrl + u'/parameters'
    printDebugMessage(u'serviceGetParameters', u'requestUrl: ' + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage(u'serviceGetParameters', u'End', 1)
    return doc[u'id':]


# Print list of parameters
def printGetParameters():
    printDebugMessage(u'printGetParameters', u'Begin', 1)
    idList = serviceGetParameters()
    for id_ in idList:
        print(id_)
    printDebugMessage(u'printGetParameters', u'End', 1)


# Get input parameter information
def serviceGetParameterDetails(paramName):
    printDebugMessage(u'serviceGetParameterDetails', u'Begin', 1)
    printDebugMessage(u'serviceGetParameterDetails', u'paramName: ' + paramName, 2)
    requestUrl = baseUrl + u'/parameterdetails/' + paramName
    printDebugMessage(u'serviceGetParameterDetails', u'requestUrl: ' + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage(u'serviceGetParameterDetails', u'End', 1)
    return doc


# Print description of a parameter
def printGetParameterDetails(paramName):
    printDebugMessage(u'printGetParameterDetails', u'Begin', 1)
    doc = serviceGetParameterDetails(paramName)
    print(unicode(doc.name) + u"\t" + unicode(doc.type))
    print(doc.description)
    if hasattr(doc, 'values'):
        for value in doc.values:
            print(value.value)
            if unicode(value.defaultValue) == u'true':
                print(u'default')
            print(u"\t" + unicode(value.label))
            if hasattr(value, u'properties'):
                for wsProperty in value.properties:
                    print(u"\t" + unicode(wsProperty.key) + u"\t" + unicode(wsProperty.value))
    printDebugMessage(u'printGetParameterDetails', u'End', 1)


# Submit job
def serviceRun(email, title, params):
    printDebugMessage(u'serviceRun', u'Begin', 1)
    # Insert e-mail and title into params
    params[u'email'] = email
    if title:
        params[u'title'] = title
    requestUrl = baseUrl + u'/run/'
    printDebugMessage(u'serviceRun', u'requestUrl: ' + requestUrl, 2)

    # Get the data for the other options
    requestData = urlencode(params)

    printDebugMessage(u'serviceRun', u'requestData: ' + requestData, 2)
    # Errors are indicated by HTTP status codes.
    try:
        # Set the HTTP User-agent.
        user_agent = getUserAgent()
        http_headers = {u'User-Agent': user_agent}
        req = Request(requestUrl, None, http_headers)
        # Make the submission (HTTP POST).
        reqH = urlopen(req, requestData.encode(encoding=u'utf_8', errors=u'strict'))
        jobId = unicode(reqH.read(), u'utf-8')
        reqH.close()
    except HTTPError as ex:
        print(xmltramp.parse(unicode(ex.read(), u'utf-8'))[0][0])
        quit()
    printDebugMessage(u'serviceRun', u'jobId: ' + jobId, 2)
    printDebugMessage(u'serviceRun', u'End', 1)
    return jobId


# Get job status
def serviceGetStatus(jobId):
    printDebugMessage(u'serviceGetStatus', u'Begin', 1)
    printDebugMessage(u'serviceGetStatus', u'jobId: ' + jobId, 2)
    requestUrl = baseUrl + u'/status/' + jobId
    printDebugMessage(u'serviceGetStatus', u'requestUrl: ' + requestUrl, 2)
    status = restRequest(requestUrl)
    printDebugMessage(u'serviceGetStatus', u'status: ' + status, 2)
    printDebugMessage(u'serviceGetStatus', u'End', 1)
    return status


# Print the status of a job
def printGetStatus(jobId):
    printDebugMessage(u'printGetStatus', u'Begin', 1)
    status = serviceGetStatus(jobId)
    if outputLevel > 0:
        print("Getting status for job %s" % jobId)
    print(status)
    if outputLevel > 0 and status == "FINISHED":
        print("To get results: python %s --polljob --jobid %s"
              "" % (os.path.basename(__file__), jobId))
    printDebugMessage(u'printGetStatus', u'End', 1)


# Get available result types for job
def serviceGetResultTypes(jobId):
    printDebugMessage(u'serviceGetResultTypes', u'Begin', 1)
    printDebugMessage(u'serviceGetResultTypes', u'jobId: ' + jobId, 2)
    requestUrl = baseUrl + u'/resulttypes/' + jobId
    printDebugMessage(u'serviceGetResultTypes', u'requestUrl: ' + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage(u'serviceGetResultTypes', u'End', 1)
    return doc[u'type':]


# Print list of available result types for a job.
def printGetResultTypes(jobId):
    printDebugMessage(u'printGetResultTypes', u'Begin', 1)
    if outputLevel > 0:
        print("Getting result types for job %s" % jobId)

    resultTypeList = serviceGetResultTypes(jobId)
    if outputLevel > 0:
        print("Available result types:")
    for resultType in resultTypeList:
        print(resultType[u'identifier'])
        if hasattr(resultType, u'label'):
            print(u"\t", resultType[u'label'])
        if hasattr(resultType, u'description'):
            print(u"\t", resultType[u'description'])
        if hasattr(resultType, u'mediaType'):
            print(u"\t", resultType[u'mediaType'])
        if hasattr(resultType, u'fileSuffix'):
            print(u"\t", resultType[u'fileSuffix'])
    if outputLevel > 0:
        print("To get results:\n  python %s --polljob --jobid %s\n"
              "  python %s --polljob --outformat <type> --jobid %s"
              "" % (os.path.basename(__file__), jobId,
                    os.path.basename(__file__), jobId))
    printDebugMessage(u'printGetResultTypes', u'End', 1)


# Get result
def serviceGetResult(jobId, type_):
    printDebugMessage(u'serviceGetResult', u'Begin', 1)
    printDebugMessage(u'serviceGetResult', u'jobId: ' + jobId, 2)
    printDebugMessage(u'serviceGetResult', u'type_: ' + type_, 2)
    requestUrl = baseUrl + u'/result/' + jobId + u'/' + type_
    result = restRequest(requestUrl)
    printDebugMessage(u'serviceGetResult', u'End', 1)
    return result


# Client-side poll
def clientPoll(jobId):
    printDebugMessage(u'clientPoll', u'Begin', 1)
    result = u'PENDING'
    while result == u'RUNNING' or result == u'PENDING':
        result = serviceGetStatus(jobId)
        if outputLevel > 0:
            print(result)
        if result == u'RUNNING' or result == u'PENDING':
            time.sleep(pollFreq)
    printDebugMessage(u'clientPoll', u'End', 1)


# Get result for a jobid
# Allows more than one output file written when 'outformat' is defined.
def getResult(jobId):
    printDebugMessage(u'getResult', u'Begin', 1)
    printDebugMessage(u'getResult', u'jobId: ' + jobId, 1)
    if outputLevel > 1:
        print("Getting results for job %s" % jobId)
    # Check status and wait if necessary
    clientPoll(jobId)
    # Get available result types
    resultTypes = serviceGetResultTypes(jobId)

    for resultType in resultTypes:
        # Derive the filename for the result
        if options.outfile:
            filename = (options.outfile + u'.' + unicode(resultType[u'identifier']) +
                        u'.' + unicode(resultType[u'fileSuffix']))
        else:
            filename = (jobId + u'.' + unicode(resultType[u'identifier']) +
                        u'.' + unicode(resultType[u'fileSuffix']))
        # Write a result file

        outformat_parm = str(options.outformat).split(',')
        for outformat_type in outformat_parm:
            outformat_type = outformat_type.replace(' ', '')

            if outformat_type == 'None':
                outformat_type = None

            if not outformat_type or outformat_type == unicode(resultType[u'identifier']):
                if outputLevel > 1:
                    print("Getting %s" % unicode(resultType[u'identifier']))
                # Get the result
                result = serviceGetResult(jobId, unicode(resultType[u'identifier']))
                if (unicode(resultType[u'mediaType']) == u"image/png"
                        or unicode(resultType[u'mediaType']) == u"image/jpeg"
                        or unicode(resultType[u'mediaType']) == u"application/gzip"):
                    fmode = 'wb'
                else:
                    fmode = 'w'

                try:
                    fh = open(filename, fmode)
                    fh.write(result)
                    fh.close()
                except TypeError:
                    fh.close()
                    fh = open(filename, "wb")
                    fh.write(result)
                    fh.close()
                if outputLevel > 0:
                    print("Creating result file: " + filename)
    printDebugMessage(u'getResult', u'End', 1)


# Read a file
def readFile(filename):
    printDebugMessage(u'readFile', u'Begin', 1)
    fh = open(filename, 'r')
    data = fh.read()
    fh.close()
    printDebugMessage(u'readFile', u'End', 1)
    return data


def print_usage():
    print("""\
EMBL-EBI Clustal Omega Python Client:

Multiple sequence alignment with Clustal Omega.

[Required (for job submission)]
  --email               E-mail address.
  --stype               Defines the type of the sequences to be aligned.
  --sequence            Three or more sequences to be aligned can be entered
                        directly into this box. Sequences can be in GCG, FASTA, EMBL
                        (Nucleotide only), GenBank, PIR, NBRF, PHYLIP or
                        UniProtKB/Swiss-Prot (Protein only) format. Partially
                        formatted sequences are not accepted. Adding a return to the
                        end of the sequence may help certain applications understand
                        the input. Note that directly using data from word
                        processors may yield unpredictable results as hidden/control
                        characters may be present. There is currently a sequence
                        input limit of 4000 sequences and 4MB of data.

[Optional]
  --guidetreeout        Output guide tree.
  --addformats          Output additional output formats.
  --dismatout           Output distance matrix. This is only calculated if the mBed-
                        like clustering guide tree is set to false.
  --dealign             Remove any existing alignment (gaps) from input sequences.
  --mbed                This option uses a sample of the input sequences and then
                        represents all sequences as vectors to these sequences,
                        enabling much more rapid generation of the guide tree,
                        especially when the number of sequences is large.
  --mbediteration       Use mBed-like clustering during subsequent iterations.
  --iterations          Number of (combined guide-tree/HMM) iterations.
  --gtiterations        Having set the number of combined iterations, this parameter
                        can be changed to limit the number of guide tree iterations
                        within the combined iterations.
  --hmmiterations       Having set the number of combined iterations, this parameter
                        can be changed to limit the number of HMM iterations within
                        the combined iterations.
  --outfmt              Format for generated multiple sequence alignment.
  --order               The order in which the sequences appear in the final
                        alignment.

[General]
  -h, --help            Show this help message and exit.
  --asyncjob            Forces to make an asynchronous query.
  --title               Title for job.
  --status              Get job status.
  --resultTypes         Get available result types for job.
  --polljob             Poll for the status of a job.
  --pollFreq            Poll frequency in seconds (default 3s).
  --jobid               JobId that was returned when an asynchronous job was submitted.
  --outfile             File name for results (default is JobId; for STDOUT).
  --outformat           Result format(s) to retrieve. It accepts comma-separated values.
  --params              List input parameters.
  --paramDetail         Display details for input parameter.
  --verbose             Increase output.
  --version             Prints out the version of the Client and exit.
  --quiet               Decrease output.
  --baseUrl             Base URL. Defaults to:
                        https://www.ebi.ac.uk/Tools/services/rest/clustalo

Synchronous job:
  The results/errors are returned as soon as the job is finished.
  Usage: python clustalo.py --email <your@email.com> [options...] <SeqFile|SeqID(s)>
  Returns: results as an attachment

Asynchronous job:
  Use this if you want to retrieve the results at a later time. The results
  are stored for up to 24 hours.
  Usage: python clustalo.py --asyncjob --email <your@email.com> [options...] <SeqFile|SeqID(s)>
  Returns: jobid

Check status of Asynchronous job:
  Usage: python clustalo.py --status --jobid <jobId>

Retrieve job data:
  Use the jobid to query for the status of the job. If the job is finished,
  it also returns the results/errors.
  Usage: python clustalo.py --polljob --jobid <jobId> [--outfile string]
  Returns: string indicating the status of the job and if applicable, results
  as an attachment.

Further information:
  https://www.ebi.ac.uk/Tools/webservices and
    https://github.com/ebi-wp/webservice-clients

Support/Feedback:
  https://www.ebi.ac.uk/support/""")


# No options... print help.
if numOpts < 2:
    print_usage()
elif options.help:
    print_usage()
# List parameters
elif options.params:
    printGetParameters()
# Get parameter details
elif options.paramDetail:
    printGetParameterDetails(options.paramDetail)
# Print Client version
elif options.version:
    print("Revision: %s" % version)
    sys.exit()
# Submit job
elif options.email and not options.jobid:
    params = {}
    if len(args) == 1 and "true" not in args and "false" not in args:
        if os.path.exists(args[0]):  # Read file into content
            params[u'sequence'] = readFile(args[0])
        else:  # Argument is a sequence id
            params[u'sequence'] = args[0]
    elif len(args) == 2 and "true" not in args and "false" not in args:
        if os.path.exists(args[0]) and os.path.exists(args[1]):  # Read file into content
            params[u'asequence'] = readFile(args[0])
            params[u'bsequence'] = readFile(args[1])
        else:  # Argument is a sequence id
            params[u'asequence'] = args[0]
            params[u'bsequence'] = args[0]
    elif hasattr(options, "sequence") or (hasattr(options, "asequence") and hasattr(options, "bsequence")):  # Specified via option
        if hasattr(options, "sequence"):
            if os.path.exists(options.sequence):  # Read file into content
                params[u'sequence'] = readFile(options.sequence)
            else:  # Argument is a sequence id
                params[u'sequence'] = options.sequence
        elif hasattr(options, "asequence") and hasattr(options, "bsequence"):
            if os.path.exists(options.asequence) and os.path.exists(options.bsequence):  # Read file into content
                params[u'asequence'] = readFile(options.asequence)
                params[u'bsequence'] = readFile(options.bsequence)
            else:  # Argument is a sequence id
                params[u'asequence'] = options.asequence
                params[u'bsequence'] = options.bsequence

    # Pass default values and fix bools (without default value)
    if options.stype:
        params['stype'] = options.stype

    if not options.guidetreeout:
        params['guidetreeout'] = 'true'
    if options.guidetreeout:
        params['guidetreeout'] = options.guidetreeout
    

    if not options.addformats:
        params['addformats'] = 'false'
    if options.addformats:
        params['addformats'] = options.addformats
    

    if not options.dismatout:
        params['dismatout'] = 'false'
    if options.dismatout:
        params['dismatout'] = options.dismatout
    

    if not options.dealign:
        params['dealign'] = 'false'
    if options.dealign:
        params['dealign'] = options.dealign
    

    if not options.mbed:
        params['mbed'] = 'true'
    if options.mbed:
        params['mbed'] = options.mbed
    

    if not options.mbediteration:
        params['mbediteration'] = 'true'
    if options.mbediteration:
        params['mbediteration'] = options.mbediteration
    

    if not options.iterations:
        params['iterations'] = 0
    if options.iterations:
        params['iterations'] = options.iterations
    

    if not options.gtiterations:
        params['gtiterations'] = -1
    if options.gtiterations:
        params['gtiterations'] = options.gtiterations
    

    if not options.hmmiterations:
        params['hmmiterations'] = -1
    if options.hmmiterations:
        params['hmmiterations'] = options.hmmiterations
    

    if not options.outfmt:
        params['outfmt'] = 'clustal_num'
    if options.outfmt:
        params['outfmt'] = options.outfmt
    

    if not options.order:
        params['order'] = 'aligned'
    if options.order:
        params['order'] = options.order
    


    # Submit the job
    jobId = serviceRun(options.email, options.title, params)
    if options.asyncjob: # Async mode
        print(jobId)
        if outputLevel > 0:
            print("To check status: python %s --status --jobid %s"
                  "" % (os.path.basename(__file__), jobId))
    else:
        # Sync mode
        if outputLevel > 0:
            print("JobId: " + jobId, file=sys.stderr)
        else:
            print(jobId)
        time.sleep(pollFreq)
        getResult(jobId)
# Get job status
elif options.jobid and options.status:
    printGetStatus(options.jobid)

elif options.jobid and (options.resultTypes or options.polljob):
    status = serviceGetStatus(options.jobid)
    if status == 'PENDING' or status == 'RUNNING':
        print("Error: Job status is %s. "
              "To get result types the job must be finished." % status)
        quit()
    # List result types for job
    if options.resultTypes:
        printGetResultTypes(options.jobid)
    # Get results for job
    elif options.polljob:
        getResult(options.jobid)
else:
    # Checks for 'email' parameter
    if not options.email:
        print('\nParameter "--email" is missing in your command. It is required!\n')

    print(u'Error: unrecognised argument combination', file=sys.stderr)
    print_usage()
