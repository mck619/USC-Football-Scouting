from bs4 import BeautifulSoup
import requests

# ESPN NCAA FOOTBALL DRIVE LOG SCRAPER
#
# Creates a CSV of the drive log from ESPN


"http://espn.go.com/college-football/playbyplay?gameId=400548172"

def scrape_log(url,name):
    r = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    s = soup.find_all("li", ["","post-play", "video"])
    f = open(name, 'w')
    for i in range(len(s)):
            dd_pos = s[i].h3.string
            play_text = s[i].span.string.replace('\n', '').lstrip() #formatting play text
            (time, play_text) = play_text.split(") ",1)             #time string has a leading ( that should be removed
            play_text = parse_play_text(play_text)
            if dd_pos:
                dd_pos = dd_pos.replace('\n', '').rstrip()          #formatted
                (dd,pos) = dd_pos.split(" at ")                     #split up into down and distance and field pos
                f.write( time[1:]+ ';' + dd + ';' + pos + ';' + play_text + '\n' )
            else:
                if 'kickoff' in s[i].span.string:
                    f.write( time[1:]+';Kickoff;Kickoff;'+ play_text + '\n')    #2 kickoffs to num cols stays good
                if 'Timeout' in play_text:
                    try:
                        dd_pos_timeout = s[i+1].h3.string.replace('\n', '').rstrip()    #need to grab DD from next play for log
                    except:
                        dd_pos_timeout = s[i+2].h3.string.replace('\n', '').rstrip()    #incase there are consecutive timeouts
                    (dd,pos) = dd_pos_timeout.split(" at ")
                    f.write( time[1:]+ ';' + dd + ';' + pos + ';' + play_text + '\n' )


    f.close()

def parse_play_text(play_text):

    gain = "NA"
    ball_carrier = "NA"
    play_type = "NA"


    if " run " in play_text:
        play_type = "RUN"
        s = play_text.split()
        ball_carrier = s[0]+ " " + s[1]

        for i in range(len(s)):
            if s[i] == "for":
                gain = s[i+1]
                break


    if " pass complete " in play_text:
        play_type = "PASS"
        s = play_text.split()
        for i in range(len(s)):
            if s[i] == "for":
                ball_carrier = s[i-2] + " " + s[i-1]
                if s[i+1] == "no":
                    gain == "0"
                else:
                    gain = s[i+1]
                break

    if " pass incomplete" in play_text:
        play_type = "INCOMPLETE PASS"
        s = play_text.split()
        for i in range(len(s)):
            if s[i] == "to":
                ball_carrier = s[i+1] + " " + s[i+2]
                break

    if " kickoff " in play_text:
        play_type = "KICKOFF"
        s = play_text.split()
        for i in range(len(s)):
            if s[i] == "return":
                ball_carrier = s[i-2] + " " + s[i-1]

    if " Timeout " in play_text:
        play_type = "TIMEOUT"
        s = play_text.split()
        ball_carrier = s[1]

    if " punt " in play_text:
        play_type = "PUNT"
        s = play_text.split()
        for i in range(len(s)):
            if s[i] == "returns":
                ball_carrier = s[i-2] + " " + s[i-1]

    if "PENALTY" in play_text:
        play_type = play_type + "(PENALTY)"

    return play_type + ";" + gain + ";" + ball_carrier + ";" + play_text

scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400548172","USCvsARKST.txt")
scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400757014","USCvsIdaho.txt")
scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400757026","USCvsStanford.txt")
scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400757037","USCvsASU.txt")
scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400757045","USCvsWASH.txt")
scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400757053","USCvsND.txt")
scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400757058","USCvsUtah.txt")
scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400757063","USCvsCal.txt")
scrape_log("http://espn.go.com/college-football/playbyplay?gameId=400757067","USCvsArizona.txt")