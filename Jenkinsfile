#!/usr/bin/env groovy
pipeline{
    agent any
    options{
        preserveStashes(buildCount: 10)
    }
    stages{
        stage('deploy taotao project'){
            environment{
                TAOTAO_DIR = """${sh(
                    returnStdout: true,
                    script: "dirname '$WORKSPACE'"
                )}""".trim()
            }
            steps{
                echo 'deploy taotao!'
                echo $WORKSPACE
                script{
                    echo "$TAOTAO_DIR"

                    dir("$TAOTAO_DIR"){
                        git credentialsId: '381e7be1-1cf0-4a2c-9577-8e4e7ab2026b', url: 'https://gitee.com/snowlts/taotao.git'
                    }

                    sh "pip install -r '$TAOTAO_DIR'/requirements.txt"
                    sh "python '$TAOTAO_DIR'/taotao/manage.py runserver &"
                }

                echo 'deploy taotao done!'
            }
        }
        stage('Test'){
            steps{
                echo "test begin"
                sh 'pip install -r requirements.txt'
                sh 'python run.py'
                echo "test end"

            }
        }
    }

    post{
        always{
            echo "build result:$currentBuild.currentResult"
            echo "test finished,please check"
            sh 'echo $WORKSPACE'
            sh 'report_dir=$WORKSPACE/report/results;if [ ! -e $report_dir ];then mkdir $report_dir;fi'
            allure includeProperties: false, jdk: '', results: [[path: 'report/results']]
            echo "send email"
            mail bcc: '',
                to: 'snowlts@163.com',
                cc: 'snowlts@126.com',
                from: 'snowlts@163.com',
                replyTo: 'snowlts@163.com',
                subject: '测试报告',
                body: "测试报告链接: <a href='http://192.168.2.133:8001/job/TaotaoInfAutomation/$BUILD_NUMBER/allure/'>请点击</a>",
                charset: 'UTF-8',
                mimeType: 'text/html'
            echo "email sent"
        }
        success{
            echo "test success"
            //deleteDir()

        }
        failure{
            echo "test failed"
        }
        unstable{
            echo "unstable:there are failed testcases"
        }
        changed{
            echo "test status changed"
        }

    }

}