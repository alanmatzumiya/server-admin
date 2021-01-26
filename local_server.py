from flask import Flask, render_template, request, redirect, url_for
import jupyter_deploy, update_containers, update_notebooks
import yaml
server = Flask(__name__, template_folder='./server-admin', static_folder='./server-admin/assets')
repos = yaml.load(open('repositories.yml'), Loader=yaml.FullLoader)

@server.route('/')
def home():


    return render_template('index.html', repos_user=repos["alanmatzumiya"], repos_org=repos["circuitalminds"], 
    containers=repos["containers"], notebooks=repos["notebooks"])

@server.route('/update/')
def update_data():
    if request.args.get("data") == "containers":
        update_containers.update_data()
    else:
        update_notebooks.update_data()
    
    return redirect(url_for('home'))
    
@server.route('/push/')
def gitpush():
    repo = request.args.get("repo")
    sentence_1 = "cd ./" + repo + " "
    sentence_2 = "&& git init && git add . && git commit -m 'auto' && git push origin main"
    #os.system(sentence_1 + sentence_2)
    
    return redirect(url_for('home'))

@server.route('/clone/')
def gitclone():
    repo = request.args.get("repo")
    #os.system("git clone " + repos[str(repo)])
    
    return redirect(url_for('home'))          

@server.route('/deploy/')
def deploynbs():
    repo = request.args.get("repo")
    #os.system("git clone " + repos[str(repo)])
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    server.run('127.0.0.1', '4000', debug=True)
