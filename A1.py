#Done by Firdaus Botirzoda

from flask import Flask
from flask import render_template
import flask
import glob
import yaml
app = Flask(__name__)
temp = {}

playID = []
Allplays = []

for fn in glob.glob('data/*.yaml'):
    with open(fn, 'r') as yf:   # load data from file fn
        play = yaml.load(yf)
       # playID = fn[5:-5]
       # play['id'] = playID
       # print(play.values())
        Allplays.append(play)   #store it away in an array
@app.route('/')
def ListingPlays():

    return flask.render_template('listingPlays.html', Allplays=Allplays)

@app.route('/play/<id>')
def PlayInfo(id):
    charactersArray = []
    for play in Allplays:
        if play['id'] == id:
            tempPlay = play  # find the specific play and store it away
    for key,value in tempPlay['characters'].items():   # store key and value from characters dictionary into array.
        charactersArray.append({'key':key,'value':value})
    return flask.render_template('playInformation.html',charactersArray = charactersArray, tempPlay=tempPlay, id=id)

@app.route('/play/<id>/acts/<int:act>/scene/<int:scene>')
def sceneInfo(id,act,scene):
    act = act - 1
    scene = scene -1
    for play in Allplays:
        if play['id'] == id:
            tempPlay = play  # find the specific play and store it away
    playTitle = tempPlay['acts'][act]['scenes'][scene]['title']
    numbers = {'actNum':act,'sceneNum':scene}
    blocks = tempPlay['acts'][act]['scenes'][scene]['blocks']

    for key, value in tempPlay['characters'].items():
        for block in blocks:
            if(key == block['speaker']):              # so im trying to make every name a link into char page
                block['value'] = value

    next = -1
    previous = -1
    try:
        a = tempPlay['acts'][act]['scenes'][scene + 1]
        next = scene + 1
    except IndexError:
        next = -1
    try:
        a = tempPlay['acts'][act]['scenes'][scene - 1]
        previous = scene - 1
    except IndexError:
        previous = -1


    return flask.render_template('sceneInformation.html',id = id, tempPlay = tempPlay,
                                 playTitle = playTitle,numbers = numbers, blocks = blocks,
                                 next = next, previous = previous)

@app.route('/characters/<characterID>')
def playsByChar(characterID):
    savedPlays = []
    for tempPlay in Allplays:
        for key, value in tempPlay['characters'].items():
            if(characterID == value):
                savedPlays.append({'characterID': characterID,'characterName':value,
                                   'playID': tempPlay['id'],'playName':tempPlay['title'],'date':tempPlay['date']})

    return flask.render_template('playsByCharacter.html', savedPlays = savedPlays)

if __name__ == '__main__':
    app.run()

