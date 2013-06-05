/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 10/18/12
 * Time: 10:20 PM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.view.ResultOptions", {
    extend: 'Ext.window.Window',
    title:'Please choose',
    layout:{
        type:'table',
        columns:2
    },
    defaults:{
        xtype:'button',
        width:150,
        height:150
    },
    items:[
        {
            text:'Download CSV Data',
            handler:function () {
                window.location = "database.php?action=csvgo";
                this.up("window").destroy();
            }
        },
        {
            text:'Open Data in Grid',
            handler:function () {
                window.open("resultgrid.html#!/" + window.reportName);
                this.up("window").destroy();
            }
        },
        {
            text:'View in Pivot Grid',
            handler:function () {
                window.open("pivot.html#!/" + window.reportName);
                this.up("window").destroy();
            }
        },
        {
            text:'Show Charting Options',
            handler:function () {
                window.open("resultgrid.html#!/" + window.reportName);
                this.up("window").destroy();
            }
        }
    ]
});