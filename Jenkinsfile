#!groovy

def sendDiscordNotification(color, message, webhookUrl) {
    def payload = [
        content: message
    ]
    def jsonPayload = groovy.json.JsonOutput.toJson(payload)
    sh "curl -H 'Content-Type: application/json' -X POST -d '${jsonPayload}' ${webhookUrl}"
}

node {
    try {
        stage('Checkout') {
            checkout scm

            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')

            // Use withCredentials to securely access the secret text
            withCredentials([string(credentialsId: 'DISCORD_WEBHOOK_URL', variable: 'DISCORD_WEBHOOK')]) {
                sendDiscordNotification("warning", "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges}", env.DISCORD_WEBHOOK)
            }
        }


        stage('Test') {
            sh 'python3.10 -m venv env'
            sh '. env/bin/activate'
            sh 'env/bin/pip install -r requirements.txt'
            sh 'env/bin/python3.10 manage.py test --testrunner=blog.tests.test_runners.NoDbTestRunner'
        }

        stage('Deploy') {
            sh 'chmod +x ./deployment/deploy_prod.sh'
            sh './deployment/deploy_prod.sh'
        }

        stage('Publish results') {
            withCredentials([string(credentialsId: 'DISCORD_WEBHOOK_URL', variable: 'DISCORD_WEBHOOK')]) {
                sendDiscordNotification("good", "Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>", env.DISCORD_WEBHOOK)
            }
        }
    } catch (err) {
        withCredentials([string(credentialsId: 'DISCORD_WEBHOOK_URL', variable: 'DISCORD_WEBHOOK')]) {
            sendDiscordNotification("danger", "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>", env.DISCORD_WEBHOOK)
        }
        throw err
    }
}