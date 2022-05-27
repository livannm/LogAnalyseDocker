# LogAnalyseCloud
 ##Installation
 
 Pour pouvoir lancer le site web et le faire fonctionner veuillez suivre ces etapes : 
 
 1. Ouvrir un terminal et se placer sur le dossier du repo
 2. Faire les 3 commandes une par une ou sur des terminaux séparés : 
                             - docker build -t docker-backend ./Docker-backend
                             - docker build -t docker-auth ./DockerAuth
                             - docker build -t docker-frontend ./DockerFront

3. Une fois que toutes les commandes on été finalisées faites la commande : docker compose up
4. Les serveurs sont lancés vous pouvez à present tester le site web
5. Sur votre navigateur taper : http://localhost:4200/
