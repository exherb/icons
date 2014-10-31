module.exports = (grunt) ->

    grunt.initConfig
        pkg: grunt.file.readJSON('package.json')
        coffee:
            files:
                {'main.coffee': 'main.js'}
        'build-atom-shell-app':
            options:
                platforms: ["darwin", "win32"]

    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-atom-shell-app-builder'
    grunt.registerTask 'default', ['coffee', 'build-atom-shell-app']
