pipeline {
    agent any
    environment {
	DB_HOST     = 'localhost'
	DB_PORT     = '3305'
	DB_NAME     = 'farpost'
	DB_USER     = 'root'
	DB_PASSWORD = '1234'
	OUTPUT_CSV = 'jenkins_logs.csv'
    }

    stages {
        stage('Extract') {
            steps {
                script {
                        import groovy.sql.Sql
                        Class.forName('com.mysql.cj.jdbc.Driver')
                        def sql = Sql.newInstance('jdbc:mysql://localhost:3305/farpost', root, 1234,
                        'com.mysql.cj.jdbc.Driver')

                        def query = 'SELECT * FROM logs'
                        sql.eachRow(query) { row ->
                            println "Time: ${row.time}, Action: ${row.column2}"
                        }

                        def statement = conn.createStatement()
                        def rs = statement.executeQuery(query)
                        def output = []

                        while(rs.next()) {
                            output.add([
                                id: rs.getInt('id'),
                                user_id: rs.getInt('user_id'),
                                action: rs.getString('action'),
                                time: rs.getTimestamp('time').toString(),
                                response: rs.getString('response'),
                                anonym: rs.getInt('anonym')
                            ])
                        }

                        conn.close()

                        env.extractedData = extractedData.collect {
                            "id:${it.id},user_id:${it.user_id},action:${it.action}," +
                            "time:${it.time},response:${it.response},anonym:${it.anonym}"
                        }

                }
            }
        }

        stage('Transform') {
            steps {
                script {
                    try {
                        def extractedData = env.extractedData.split('\\|').collect { entry ->
                            def map = [:]
                            entry.split(',').each { pair ->
                                def (key, value) = pair.split(':', 2)
                                map[key.trim()] = value.trim()
                            }
                            return map
                        }

                        def transformedData = []
                        def dateFormat = new java.text.SimpleDateFormat("yyyy-MM-dd")

                        extractedData.each { row ->
                            def userCreatedStr = row.user_created.replace('T', ' ').replace('Z', '')
                            def actionTimeStr = row.action_time.replace('T', ' ').replace('Z', '')

                            def userCreated = dateFormat.parse(userCreatedStr)
                            def actionTime = dateFormat.parse(actionTimeStr)

                            output.add([
                                id: rs.getInt('id'),
                                user_id: rs.getInt('user_id'),
                                action: rs.getString('action'),
                                time: rs.getTimestamp('time').toString(),
                                response: rs.getString('response'),
                                anonym: rs.getInt('anonym')
                            ])

                            env.extractedData = extractedData.collect {
                                "id:${it.id},user_id:${it.user_id},action:${it.action}," +
                                "time:${it.time},response:${it.response},anonym:${it.anonym}"
                        }
                    }
                }
            }
        }

        stage('Load') {
            steps {
                script {
                    try {
                        // Восстанавливаем данные из строки
                        def transformedData = env.transformedData.split('\\|').collect { entry ->
                            def map = [:]
                            entry.split(',').each { pair ->
                                def (key, value) = pair.split(':', 2)
                                map[key.trim()] = value.trim()
                            }
                            return map
                        }

                        // Создаем CSV файл
                        def csvHeader = 'id,user_id,action,time,response,anonym'
                        def csvLines = transformedData.collect { row ->
                            "${row.id},\"${row.user_id}\",${row.action},${row.time},${row.response},${row.anonym}"
                        }

                        writeFile file: env.OUTPUT_CSV, text: ([csvHeader] + csvLines).join('\n')
                        archiveArtifacts artifacts: env.OUTPUT_CSV, onlyIfSuccessful: true
                    }
                }
            }
        }
    }
}
//                     //Кол-во созданных аккаунтов
//                     def query_new_accs = """
//                     SELECT count(action) FROM logs WHERE DATE(time)<"2025-02-25" and
//                         Date(time)>"2025-02-05" and action like 'registration' group by date(time);
//                     """
//
//                     //Кол-во сообщений всего
//                     def query_all_messages_count = """
//                     SELECT count(action) FROM logs WHERE DATE(time)<"2025-02-25" and
//                         Date(time)>"2025-02-05" and action like 'create_message' group by date(time);
//                     """
//
//                     //Кол-во сообщений Анонимов
//                     def query_anonym_messages_count = """
//                     SELECT count(action) FROM logs WHERE DATE(time)<"2025-02-25" and
//                         Date(time)>"2025-02-05" and action like 'create_message' and anonym = 1 group by date(time);
//                     """
//
//                     //Кол-во тем на форуме
//                     def query_create_theme_amount = """
//                     SELECT count(action) FROM logs WHERE DATE(time)<"2025-02-25" and
//     ->                  Date(time)>"2025-02-05" and action like 'create_theme' group by date(time);
//                     """
                    }
                }
            }
        }
    }