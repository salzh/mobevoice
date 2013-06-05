/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 3:14 AM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.view.SavedQueries", {
    extend:'Ext.window.Window',
    id:'SavedQueryWindow',
    title:'Saved Queries',
    alias:'widget.savedqueries',
    layout:'fit',
    items:[
        {
            xtype:'combo',
            store:'SavedQuery',
            displayField:'name',
            id:'SavedQueriesCombo',
            width:300,
            emptyText:'Select a Query to Start Downloading',
            valueField:'name',
            listeners:{
                change:function (box, value) {
                    if (value.length < 1) {
                        return;
                    }

                    var limitwin = Ext.create("Ext.window.Window", {
                        title:'Query : ' + value,
                        layout:'anchor',
                        items:[
                            {
                                xtype:'label',
                                html:'<h3>' + value + "</h3>"
                                //fieldLabel:'Query'
                            },
                            {
                                xtype:'combo',
                                label:'Limit',
                                emptyText:'500',
                                id:'rowLimit',
                                store:Ext.create("Ext.data.Store", {
                                    fields:[
                                        'name',
                                        'value'
                                    ],
                                    data:[
                                        {'name':'100', 'value':'100'},
                                        {'name':'200', 'value':'200'},
                                        {'name':'500', 'value':'500'},
                                        {'name':'1000', 'value':'1000'},
                                        {'name':'2000', 'value':'2000'},
                                        {'name':'5000', 'value':'5000'},
                                        {'name':'10000', 'value':'10000'},
                                        {'name':'20000', 'value':'20000'}
                                    ]
                                }),
                                displayField:'name',
                                valueField:'value'
                            }
                        ],
                        bbar:[
                            {
                                xtype:'tbfill'
                            },
                            {
                                xtype:'button',
                                text:'Okay',
                                handler:function () {
                                    Ext.getCmp("SavedQueriesCombo").setValue("");
                                    var rowLimit = Ext.getCmp("rowLimit").getValue();
                                    if (!rowLimit || rowLimit.length < 1) {
                                        rowLimit = 500;
                                    }
                                    rowLimit = parseInt(rowLimit);
                                    limitwin.mask("Requesting Saved Report");

                                    Zenoreport.SavedQueryFetch.getSavedQuery(value, rowLimit, function () {
                                        limitwin.destroy();
                                        window.reportName = value;
                                        var win = Ext.create("Zenoreport.view.ResultOptions");
                                        win.show();
                                    });
                                }
                            }
                        ],
                        listeners:{
                            afterrender:function () {
                                Ext.getCmp("rowLimit").expand(true);
                            }
                        }
                    });
                    limitwin.show();


                    /*Ext.Msg.prompt('Limit', 'Please enter Row Limit \nEmpty for 20000', function (btn, txt) {
                     if (btn == "ok") {
                     if (!txt || txt.length < 1) {
                     txt = 20000;
                     }
                     txt = parseInt(txt);

                     }
                     });*/

                },
                afterrender:function () {
                    this.doQuery(this.allQuery, true);
                    this.expand();
                }
            }
        }
    ]
})
;