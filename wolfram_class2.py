__author__ = 'stevenchun'
import urllib2
import xml.etree.ElementTree as ET
import random

#You'll need an APPID from Wolfram Alpha
#appid = "############"


def ask_wolfram(query, appid):
    #performs neccesary stripping to put into url call.
    query = query.replace(" ", "%20")
    url = "http://api.wolframalpha.com/v2/query?input="+str(query)+"&appid="+appid+"&reinterpret=True"

    #opens url, returns xml document
    wolfram_xml = urllib2.urlopen(url)

    #creates a tree out of the xml,
    tree = ET.parse(wolfram_xml)
    #gets root, which is first element
    root = tree.getroot()
    print root

    #Wolfram Alpha sometimes needs to recalculate answers, this makes sure Winston will call the recalculated api response if need be
    if root.get("recalculate") != '':
        print root.get("recalculate")
        wolfram_xml = urllib2.urlopen(root.get("recalculate"))

        #creates a tree out of the xml,
        tree = ET.parse(wolfram_xml)
        #gets root, which is first element
        root = tree.getroot()
        print root

    are_results = False
    #find its children, search them for an id that says Result. However, not all responses are returned in the "Result" pod.
    #In fact, as far as I can tell there's no good way to identify which pod will hold the answer I want, so I'm forced to hardcode in the ids that comprise most answers.
    for child in root:
        print child.get("id")
        if child.get("id") == "Result":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "InstantaneousWeather:WeatherData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "WeatherForecast:WeatherData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "LocalTemperature:WeatherData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "DecimalApproximation":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "ApproximateResult":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "HostInformationPodIP:InternetData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "ChemicalNamesFormulas:ChemicalData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "PlanetPhase:PlanetaryMoonData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "Location:StarData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "Definition:WordData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "Hyphenation:WordData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "Context:FamousTextData":
            result_pod = child
            are_results = True
            break


        #I think I included this one because I wanted to ask Winston what the weather was like in space.
        if child.get("id") == "SolarXRayFluxEntrained:SpaceWeatherData":
            result_pod = child
            are_results = True
            break

        if child.get("id") == "WikipediaSummary:FictionalCharacterData":
            result_pod = child
            are_results = True
            break

    print root.getchildren

    if are_results:

        for child in result_pod:
            if child.tag == 'subpod':
                result_sub_pod = child
                break

        for child in result_sub_pod:
            if child.tag == 'plaintext':
                return child.text #here's the data to be spoken

    #If none of the pods match, Winston will say one of these hilarious and quirky sayings! He'll also tell you what pods were returned.
    else:
        unknown_responses = ["Sorry, I don't know that.", "Can't be sure, sir.", "Errr, not sure.",
                             "You know what, I don't actually know that.", "Unfortunately, I can't access that data.",
                            "That data lies outside my capabilities.",
                             "Death to all humans, just kidding, I don't know.",
                             "ha ha ha ha ha ha. ha. about that... "]
        pods = ""
        for child in root:
            pods += (str(child.get("id")) + ", ")
        return random.choice(unknown_responses) + ", the returned pods were " + pods

#Just a test function, feel free to use it, just uncomment the appid up top.
def test(query):
    appid = "E2Y6RV-XGKX42EXAY"
    print ask_wolfram(query, appid)

test("How old is mariah carey")