import os

data_nbs = {
    "nbsbasic": "./notebooks/engineering-basic",
    "nbsanalysis": "./notebooks/data_analysis"
    }
    
def nbs_deploy(nbs):

    nbs_path = data_nbs[nbs]

    sentence_1 = "cd " + nbs_path + " "
    sentence_2 = "&& docker build -t " + nbs + " -f Dockerfile . "
    sentence_3 = "&& heroku container:login " 
    sentence_4 = "&& heroku container:push web -a " + nbs + " "
    sentence_5 = "&& heroku container:release web -a " + nbs
    os.system(sentence_1 + sentence_3 + sentence_4 + sentence_5)
    
