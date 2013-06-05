/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 1:02 AM
 * To change this template use File | Settings | File Templates.
 */

Ext.define("Zenoreport.Toolbar", {
    /*requires: [
     'Zenoreport.model.Schema',
     'Zenoreport.model.Schemas'
     ],*/
    extend:'Ext.toolbar.Toolbar',
    alias:'widget.zenoreporttoolbar',
    items:[
        {
            text:'New Query',
            handler:function () {
                Ext.ComponentQuery.query("window").forEach(function (win) {
                    if (win.id.substr(0, 6) == "window") {
                        win.destroy();
                    }
                });
                if (Ext.getCmp("relationWindow")) {
                    Ext.getCmp("relationWindow").destroy();
                }
                window.events = [];
                window.allgroupby = false;
            }
        },
        {
            text:'Show Relations',
            handler:Zenoreport.Function.showRelationWindow
        },
        {
            text:'Result',
            listeners:{
                click:function () {
                    var data = {};
                    data.c = [];
                    window.x = Ext.getCmp("selectedColumns");
                    var items = Ext.getCmp("selectedColumns").items;
                    var tables = [];
                    for (var i = 1; i < items.length; i++) {

                        var item = items.get(i);

                        var sel = {};
                        sel.fn = item.items.get(0).getValue();
                        sel.a = item.items.get(1).getValue();
                        sel.tn = item.items.get(2).getValue();
                        if (tables.indexOf(sel.tn) < 0) {
                            tables.push(sel.tn);
                        }
                        sel.t = 0;
                        sel.s = item.items.get(3).getValue();
                        sel.d = item.items.get(4).getValue();
                        sel.o1 = item.items.get(5).getValue();
                        sel.o2 = item.items.get(6).getValue();
                        sel.o3 = item.items.get(7).getValue();
                        sel.ag = item.items.get(8).getValue();
                        sel.gb = item.items.get(9).getValue();
                        sel.colName = item.items.get(10).getValue();
                        data.c.push(sel);
                    }
                    data.r = relations;
                    data.e = tables;

                    Ext.Ajax.request({
                        url:'database.php',
                        params:{
                            q:Ext.JSON.encode(data),
                            action:'doRetrieve'
                        },
                        success:function (result) {
                            console.log(result);
                            result = Ext.JSON.decode(result.responseText);
                            if (!result.result || result.result != "success") {
                                Ext.Msg.alert("Error", "There was some error while forming the query :: \n" + result.error);
                            } else if (result.sql.length < 10) {
                                Ext.Msg.alert("Error", "No Query is Formed");
                            } else {
                                var win = Ext.create("Zenoreport.view.ResultOptions");
                                win.show();
                            }
                        }
                    });
                }
            }
        },
        {
            text:'Tables',
            id:'showTables',
            listeners:{
                click:function () {
                    var eWin = Ext.get("tablesWindow");
                    if (eWin) {
                        eWin.show();
                        return;
                    }


                    var win = Ext.create('Zenoreport.view.SelectTableGrid');
                    var body = Ext.getCmp("zenoreportBody");
                    body.add(win);
                    win.show();
                }
            }
        },
        {
            text:'Save Query',
            handler:function () {
                Ext.Msg.prompt("Query Title", 'Please Enter query Name', function (btn, text) {
                    if (btn == "ok") {
                        Ext.Ajax.request({
                            url:'database.php?action=saveQuery&name=' + text,
                            success:function (response) {
                                if (response.responseText == "success") {
                                    Ext.Msg.alert("Saved", "Query Saved \n" + text);
                                }
                            }
                        });
                    }
                });
            }
        },
        {
            text:'Export CSV',
            handler:function () {
                window.location = "database.php?action=csvgo";
            }
        },
        {
            text:'Show Saved Queries',
            id:'btnShowSavedQueries',
            handler:function () {
                var win = Ext.create("Zenoreport.view.SavedQueries");
                win.show();
                win.alignTo(Ext.getBody(), "tr-tr", [-10, 30]);
            }
        },
        {
            text:'Pivot Grid',
            handler:function () {
                window.open("pivot.html");
            }
        },
        {
            xtype:'tbfill'
        },
        {
            text:'Enter Query Manually',
            handler:function () {
                var editor;
                var win = Ext.create("Ext.window.Window", {
                    title:'Enter SQL',
                    layout:'fit',
                    width:500,
                    height:300,
                    id:'SqlTextArea',
                    defaults:{
                        width:500
                    },
                    items:[
                        {
                            xtype:'panel',
                            layout:'fit',
                            items:[
                                {
                                    xtype:'textarea',
                                    id:'sqltext',
                                    html:'Select\n* \nFrom',
                                    listeners:{
                                        afterrender:function (txt) {
                                            console.log(txt);
                                            window.editor = CodeMirror.fromTextArea(txt.el.dom, {
                                                mode:"text/x-mysql",
                                                tabMode:"indent",
                                                matchBrackets:true
                                            });
                                            /*window.editor.setValue('select \n' +
                                                's.id, \n' +
                                                's.`name` as `name`,\n' +
                                                'sss.ani, \n' +
                                                'ss.`name` as `status` ,\n' +
                                                's.balance ,\n' +
                                                'c.`name` as `carriername`\n' +
                                                'from service s\n' +
                                                'join service_status ss on s.status = ss.id\n' +
                                                'join service_signin sss on sss.service_id=s.id\n' +
                                                'join carrier_cache_data247 ccd on sss.ani=ccd.number\n' +
                                                'join carrier c on c.id=ccd.carrier_id\n' +
                                                'order by s.id desc\n'
                                            );*/
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    bbar:[
                        {xtype:'tbfill'},
                        {
                            text:'Okay',
                            handler:function () {
                                var sql = window.editor.getValue();
                                Ext.Ajax.request({
                                    method:'POST',
                                    url:'parseSql.php',
                                    params:{
                                        sql: sql
                                    },
                                    success:function (response) {
                                        console.log(response.responseText);
                                        var data = Ext.JSON.decode(response.responseText);

                                        if (data.result && data.result == "error") {
                                            Ext.Msg.alert("Error", data.error);
                                        }

                                        var items = [];
                                        for (var i = 0; i < data.length; i++) {
                                            var c = Ext.create("widget.panel", {
                                                //xtype: 'panel',
                                                layout:'anchor',
                                                items:[
                                                    {
                                                        xtype:'textfield',
                                                        fieldLabel:'Base Expression',
                                                        value:data[i].base,
                                                        readOnly:true
                                                    },
                                                    {
                                                        xtype:'textfield',
                                                        fieldLabel:'Alias',
                                                        value:data[i].alias,
                                                        readOnly:true
                                                    },
                                                    {
                                                        xtype:'combo',
                                                        fieldLabel:'Type',
                                                        alias:'typeofData',
                                                        store:Ext.create("Ext.data.Store", {
                                                            fields:['name', 'value'],
                                                            data:[
                                                                {name:'String', value:'string'},
                                                                {name:'Integer', value:'int'},
                                                                {name:'Date or Time', value:'datetime'}
                                                            ]
                                                        }),
                                                        displayField:'name',
                                                        valueField:'value',
                                                        queryMode:'local',
                                                        value:'string'
                                                    }
                                                ]
                                            });
                                            items.push(c);
                                            //cp.add(c);
                                        }
                                        window.items = items;
                                        var win2 = Ext.create("Ext.window.Window", {
                                            title:'Select Column Datatypes',
                                            id:'columnsType',
                                            layout:'anchor',
                                            autoScroll:true,
                                            height:400,
                                            items:items,
                                            bbar:[
                                                {
                                                    xtype:'button',
                                                    text: 'Query',
                                                    handler:function () {
                                                        var data = [];
                                                        for (var i = 0; i < window.items.length; i++) {
                                                            data.push({
                                                                name:window.items[i].down("textfield").next("textfield").value,
                                                                type:window.items[i].down("combo").value
                                                            });
                                                        }
                                                        Ext.Ajax.request({
                                                            url:'database.php',
                                                            params:{
                                                                action:'customQuery',
                                                                data:Ext.JSON.encode(data),
                                                                query: sql
                                                            },
                                                            success:function (response) {
                                                                var win = Ext.create("Zenoreport.view.ResultOptions");
                                                                win.show();
                                                            }
                                                        });
                                                    }
                                                }
                                            ]
                                        });
                                        win.destroy();
                                        win2.show();
                                        win2.setSize(null, 400);
                                    }
                                });
                            }
                        }
                    ]
                });
                win.show();
            }
        }
    ],
    initComponent:function () {
        Ext.apply(this, {
            items:this.items
        });

        this.superclass.initComponent.apply(this, arguments);
    }

});

//Ext.reg('zenoreporttoolbar', Zenoreport.Toolbar);
