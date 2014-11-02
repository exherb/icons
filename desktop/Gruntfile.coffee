module.exports = (grunt) ->

    grunt.initConfig
        pkg: grunt.file.readJSON('package.json')
        coffee:
            compile:
                files:
                    {'main.js': 'main.coffee'}
        copy:
            mac:
                files:[
                    {src: 'index.html', dest: 'resources/mac/Icons.app/Contents/Resources/app/index.html'},
                    {src: 'main.js', dest: 'resources/mac/Icons.app/Contents/Resources/app/main.js'},
                    {src: 'package.json', dest: 'resources/mac/Icons.app/Contents/Resources/app/package.json'},
                    {expand: true, cwd: '../build', src: ['*'], dest: 'resources/mac/Icons.app/Contents/Resources/app/icons', filter: 'isFile'}
                ]
            windows:
                files:[
                    {src: 'index.html', dest: 'resources/windows/Icons/resources/app/index.html'},
                    {src: 'main.js', dest: 'resources/windows/Icons/resources/app/main.js'},
                    {src: 'package.json', dest: 'resources/windows/Icons/resources/app/package.json'}
                ]
        chmod: 
            options:
                mode: '755'
            mac:
                src: ['resources/mac/Icons.app/Contents/Resources/app/icons/*.so', 'resources/mac/Icons.app/Contents/Resources/app/icons/icons']

    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-copy'
    grunt.loadNpmTasks 'grunt-chmod'
    grunt.registerTask 'default', ['coffee', 'copy', 'chmod']
