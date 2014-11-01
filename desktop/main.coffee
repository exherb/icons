app = require 'app'
BrowserWindow = require 'browser-window'

require('crash-reporter').start()

app.on 'window-all-closed', ->
    app.quit()

app.on 'ready', ->
    width = 300 + 10*2 + 10*2 + 20;
    height = width + 5 + 50
    mainWindow = new BrowserWindow
        width: width
        height: height
        resizable: false
        center: true
        show: false

    dialog = require 'dialog'
    ipc = require 'ipc'
    is_setting_output = false
    output_directory = null
    ipc.on 'output-setting', ()->
        if is_setting_output
            return
        is_setting_output = true
        dialog.showOpenDialog
            title: 'Choose output directory'
            properties: [ 'openDirectory']
        , (directories)->
            if directories and directories.length > 0
                output_directory = directories[0]
            else
                output_directory = null
            mainWindow.webContents.send 'output-seted', output_directory
            is_setting_output = false


    ipc.on 'icon-droped', (event, path)->
        spawn = require('child_process').spawn
        args = [path]
        if output_directory
            args.push '-o'
            args.push output_directory
        icons = spawn(__dirname + '/icons/icons', args)
        icons.stdout.on 'data', (data)->
            console.log 'stdout: ' + data
        icons.stderr.on 'data', (data)->
            console.log 'stderr: ' + data
        icons.on 'exit', (code)->
            if code == 0
                dialog.showMessageBox
                    type: 'info'
                    buttons: ['OK']
                    title: 'Success'
                    message: 'Your icons is ready to go'
        icons.unref()

    mainWindow.loadUrl 'file://' + __dirname + '/index.html'
    mainWindow.webContents.on 'did-finish-load', ->
        mainWindow.show()

    mainWindow.on 'closed', ->
        mainWindow = null
