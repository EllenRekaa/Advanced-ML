#!/usr/bin/python

import csv
import getopt
import json
import sys

try:
    from urllib.request import Request, urlopen  # Python 3
except ImportError:
    from urllib2 import Request, urlopen  # Python 2


def usage():
    print()
    print("Get observations from the NVE Hydrological API (HydAPI)")
    print("Parameters:")
    print("   -a: ApiKey (mandatory). ")
    print("   -s: StationId (mandatory). Several stations can be given separated by comma. Example \"6.10.0,12.209.0")
    print("   -p: Parameter (mandatory). Several Parameters can be given se")
    print("   -r: Resolution time. 0 (instantenous),60 (hourly) or 1440 (daily). (mandatory)")
    print("   -t: Reference time. See documentation for referencetime. Example \"P1D/\", gives one day back in time. If none given, the last observed value will be returned")
    print("   -h: This help")
    print()
    print("Example:")
    print("    python get-observations.py -a \"INSERT_APIKEY_HERE\" -s \"6.10.0,12.209.0\" -p \"1000,1001\" -r 60 -t \"P1D/\"")
    print()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "a:s:p:r:ht:")
    except getopt.GetoptError as err:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    station = None
    parameter = None
    resolution_time = None
    api_key = None
    reference_time = None

    for opt, arg in opts:
        if opt == "-s":
            station = arg
        elif opt == "-p":
            parameter = arg
        elif opt == "-r":
            resolution_time = arg
        elif opt == "-a":
            api_key = arg
        elif opt == "-t":
            reference_time = arg
        elif opt == "-h":
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"

    if api_key == None:
        print("Error: You must supply the api-key with your request (-a)")
        usage()
        sys.exit(2)

    if station == None or parameter == None or resolution_time == None:
        print("Error: You must supply the parameters station (-s), parameter (-p) and resolution time (-r)")
        usage()
        sys.exit(2)

    baseurl = "https://hydapi.nve.no/api/v1/Observations?StationId={station}&Parameter={parameter}&ResolutionTime={resolution_time}"

    url = baseurl.format(station=station, parameter=parameter,
                         resolution_time=resolution_time)

    if reference_time is not None:
        url = "{url}&ReferenceTime={reference_time}".format(
            url=url, reference_time=reference_time)

    print(url)

    request_headers = {
        "Accept": "application/json",
        "X-API-Key": api_key
    }

    request = Request(url, headers=request_headers)

    response = urlopen(request)
    content = response.read().decode('utf-8')

    parsed_result = json.loads(content)

    for observation in parsed_result["data"]:
        print(observation)


if __name__ == "__main__":
    main(sys.argv[1:])
    
    

#Info om vassdragsnummer mm

    # Vassdragsnummeret gjenspeiler den hydrologiske strukturen i et nedbørfelt, 
    # og gir informasjon om hvor mange nivåer den overordnete enheten er delt i. 
    # Inndelingssystemet er stringent, men åpent slik at nye enheter på laveste 
    # nivå i hierarkiet kan deles inn og kodes etter samme enhetlige systematikk.
    # Områdegrensene mellom minsteenhetene er tegnet på papirkart fra kartserien 
    # Norge 1: 50.000 og er digitalisert derfra. Alle enheter er avgrenset ved 
    # to punkt på kartet, enten øverst og nederst langs elvestrengen i enheten, 
    # eller ytterpunktene langs en kyststrekning (kystfelt)

    # Norge er delt inn i 262 vassdragsområder. Et vassdragsområde er landarealet 
    # som omfatter nedbørfeltene til alle små og store vassdrag som drenerer til 
    # havet innenfor et kystavsnitt. Vassdrag som drenerer ut av Norge over 
    # riksgrensen, er også samlet i vassdragsområder.
    
    #Header 
    #['objektType', 'vassdragsnummer', 'lokalNavn', 'regineAreal_km2',
    #'nedborfeltOppstromAreal_km2', 'elvNavnHierarki',
    #'QNormalRegine_Mm3Aar', 'QNedborfeltOppstrom_Mm3Aar',
    #'nedborfeltVassdragNrOverordnet', 'overordnetNedborfeltNavn',
    #'nedbfeltHavVassdragNr', 'nedborfeltTilHav', 'hierarkiNivaRegine',
    #'punktNavnFra', 'punktNavnTil', 'QNormalr6190_lskm2',
    #'QNormal3060_lskm2', 'statistikkomrNr', 'dataUttaksdato', 'eksportType',
    #'SHAPE_Length', 'SHAPE_Area', 'geometry']
    
    #c['vassdragsnummer'][1:20]
    # 1       159.32A0
    # 2        159.32B
    # 3       159.32AA
    # 4      161.1A2AB
    # 5       055.D42B
    # 6        206.B3B
    # 7       022.EA4B
    # 8       078.4B1B
    # 9       076.G61B
    # 10     067.2D2AB
    # 11    012.BB4A1C
    # 12     167.BB21B
    # 13    036.B51A2B
    # 14     076.D5AAB
    # 15    021.GB112B
    # 16      067.3BB4
    # 17      067.3BB3
    # 18     104.C711B
    # 19        209.4D