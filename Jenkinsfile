podTemplate(yaml: """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:1.11
    command: ['cat']
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  - name: kubedeployer
    image: widerin/eks-helmsman:0.2
    command: ['cat']
    tty: true
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
"""
) {

    def image = "aemel/simple-flask-1:${currentBuild.number}"
    node(POD_LABEL) {

        stage('Verify code') {

            echo "*** TODO ***"
            echo "Here is where unit tests, pep8 or Sonarqube verification should happen"
            echo "*** TODO ***"
        }

        stage('Build Docker image') {
            git 'https://github.com/aemelius/simple-flask-1.git'
            container('docker') {
                sh "docker build -t ${image} ."
	       	      withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'USER', passwordVariable: 'PASSWORD']]) {

                    sh "docker login -u ${USER} -p ${PASSWORD}"
                    sh "docker push ${image}"
                }
            }
        }

	      stage('Kubectl stuff') {
            git 'https://github.com/aemelius/simple-flask-1.git'
	          container('kubedeployer') {
	       	      withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'kubedeployer1', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY']]) {
	       	          withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'db', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD']]) {

                        sh """sed -i "s|@@@IMAGE@@@|${image}|g" ./kube/deployment.yaml"""
                        sh """sed -i "s|@@@DB_USER@@@|${DB_USER}|g" ./kube/deployment.yaml"""
                        sh """sed -i "s|@@@DB_PASSWORD@@@|${DB_PASSWORD}|g" ./kube/deployment.yaml"""

			                  sh "aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}"
			                  sh "aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}"
			                  sh "aws eks update-kubeconfig --name=sb1 --region=eu-west-2"
                        sh "kubectl apply -f ./kube/namespace.yaml"
                        sh "kubectl apply -f ./kube/deployment.yaml"
                        sh "kubectl apply -f ./kube/service.yaml"
                        sh "kubectl apply -f ./kube/ingress.yaml"
                        sh "kubectl get ingress -n simple-flask-1 -o json"
                    }
                }
			      }
	      }
	  }

}
