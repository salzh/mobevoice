/*!
 * Ext JS Library 3.4.0
 * Copyright(c) 2006-2011 Sencha Inc.
 * licensing@sencha.com
 * http://www.sencha.com/license
 */
Ext.ns('pivot');

Ext.Ajax.timeout = 900000;
Ext.Ajax.on('requestexception', function (conn, response, options) {
    if (response.status === 302) {
        window.location = 'login.html';
    }
});
Ext.onReady(function () {
    var hash = document.location.hash;
    if (hash.substr(2).length > 0) {
        var report = document.location.hash.substr(2).split("/");
        if (report.length == 3) {
            Zenoreport.SavedQueryFetch.getSavedQuery(report[1], report[2], makePivot);
            return;
        } else {
            makePivot();
        }
    } else {
        makePivot();
    }
    document.location.hash = document.location.hash.replace(/ /g, "+");
});

function makePivot() {
    Ext.Ajax.request({
        url:'database.php',
        params:{
            action:'getLastRequest',
            mode:'OnlyMeta'
        },
        success:function (result) {
            var text = result.responseText;
            try {
                result = Ext.JSON.decode(text);
            } catch (err) {
                Ext.Msg.alert(
                    "Error",
                    "Pivot Data not available, This SQL was not Generated using Zenoreport.\\nYou can Only Download CSV Data",
                    function () {
                        window.close();
                    });
                return;
            }


            if (result.result != "success") {
                Ext.Msg.alert({
                    title:'Something failed',
                    msg:result.error,
                    icon:Ext.Msg.ERROR,
                    buttons:Ext.Msg.OK
                });
                console.log(result);
                return;
            }

            window.gridData = result;
            var gridCols = [];
            result.columnsData.forEach(function (c) {
                gridCols.push({name:c.name, header:c.name, dataIndex:c.name, type:c.type});
            });

            Ext.define('pivot.SaleRecord', {
                extend:'Ext.data.Model',
                fields:gridCols
            });

            var myStore = new Ext.data.Store({
                autoLoad:true,
                model:'pivot.SaleRecord',
                //data:result.data
                proxy:{
                    type:'ajax',
                    url:'database.php?action=getLastRequest&mode=all',
                    reader:{
                        type:'json',
                        root:'data'
                    }
                }
            });
            myStore.proxy.timeout = 600000;

            window.myStore = myStore;

            var featureSummary = Ext.create('Ext.ux.grid.feature.mzPivotSummary', {
                idItem:'fs'
            });
            /*var exportButton = new Ext.ux.Exporter.Button({
             text:"Download as .xls"
             });*/
            var pivotGrid = Ext.create('Ext.ux.grid.mzPivotGrid', {
                store:myStore,
                region:'center',
                margins:'5 5 5 0',
                enableLocking:true,
                viewConfig:{
                    trackOver:true,
                    stripeRows:false
                },
                tbar:[
                    {
                        xtype:'button',
                        text:'Expand all',
                        handler:function () {
                            pivotGrid.expandAll();
                        }
                    },
                    {
                        xtype:'button',
                        text:'Collapse all',
                        handler:function () {
                            pivotGrid.collapseAll();
                        }
                    },
                    //exportButton,
                    {
                        xtype:'button',
                        text:'Export',
                        handler:function () {
                            var finaldata = [];
                            Ext.ComponentQuery.query("grid")[1].getStore().data.items.forEach(function (d) {
                                finaldata.push(d.data)
                            });
                            finaldata = Ext.JSON.encode(finaldata);
                            Ext.Ajax.request({
                                url:'tocsv.php',
                                params:{
                                    data:finaldata,
                                    pivotData:Ext.JSON.encode(window.pivotData)
                                },
                                success:function () {
                                    console.log("done");
                                }
                            });
                            /*var ewin = Ext.create("Ext.window.Window", {
                             title:'Export as',
                             layout:{
                             type:'table',
                             columns:2
                             },
                             items:[
                             {
                             xtype:'button',
                             text:'as XLS',
                             handler:function () {

                             }
                             }
                             ]
                             });
                             ewin.show();*/
                        }
                    },
                    {
                        xtype:'button',
                        text:'Notes',
                        handler:function () {
                            if (!window.savedPivot) {
                                Ext.Msg.alert({
                                    title:'No Pivot Loaded',
                                    msg:'No Saved Pivot is loaded'
                                });
                                return;
                            }
                            var notewindow = Ext.create("Ext.window.Window", {
                                title:'Note',
                                width:300,
                                height:300,
                                layout:'fit',
                                items:[
                                    {
                                        xtype:'htmleditor',
                                        id:'note'
                                    }
                                ],
                                bbar:[
                                    {
                                        xtype:'tbfill'
                                    },
                                    {
                                        xtype:'button',
                                        text:'Save',
                                        handler:function () {
                                            Ext.Ajax.request({
                                                url:'database.php',
                                                params:{
                                                    action:'savePivotNote',
                                                    note:Ext.getCmp("note").getValue(),
                                                    pivot:window.savedPivot
                                                },
                                                success:function (d) {
                                                    d = d.responseText;
                                                    if (d == "success") {
                                                        Ext.Msg.alert({
                                                            title:'Saved',
                                                            msg:'Note Was Saved'
                                                        });
                                                    } else {
                                                        Ext.Msg.alert({
                                                            title:'Failed',
                                                            msg:'Note Was NOT Saved, Please try again.'
                                                        });
                                                    }
                                                }
                                            })
                                        }
                                    }
                                ]
                            });
                            notewindow.show();

                            notewindow.mask();
                            Ext.Ajax.request({
                                url:'database.php?action=getPivotNote',
                                params:{
                                    pivot:window.savedPivot
                                },
                                success:function (D) {
                                    notewindow.unmask();
                                    var data = Ext.JSON.decode(D.responseText);
                                    if (data.success) {
                                        Ext.getCmp("note").setValue(data.text);
                                    } else {
                                        Ext.Msg.alert({
                                            title:'Error',
                                            msg:'Error while loading the Note'
                                        });
                                    }
                                },
                                error:function () {
                                    notewindow.unmask();
                                    Ext.Msg.alert({
                                        title:'Error',
                                        msg:'Error while loading the Note'
                                    });
                                }
                            });
                        }
                    }
                ],
                features:[featureSummary],
                aggregate:[
                    /*{
                     measure:'value',
                     header:'Value',
                     aggregator:'sum',
                     align:'right',
                     width:80,
                     renderer:Ext.util.Format.numberRenderer('0,000.00')
                     },
                     {
                     measure:'quantity',
                     header:'Qnt',
                     aggregator:'sum',
                     align:'right',
                     width:80,
                     renderer:Ext.util.Format.numberRenderer('0,000.00')
                     }*/
                ],

                leftAxisTitle:'Some report',
                leftAxis:[
                    /*{
                     width:80,
                     dataIndex:'person',
                     header:'Person'
                     },
                     {
                     width:90,
                     dataIndex:'product',
                     header:'Product'
                     },
                     {
                     width:90,
                     dataIndex:'month',
                     header:'Quarter',
                     direction:'DESC'
                     }*/
                ],

                topAxis:[
                    /*{
                     dataIndex:'year',
                     header:'Year',
                     direction:'DESC'
                     },
                     {
                     dataIndex:'city',
                     header:'City'
                     }*/
                ]
            });

            var configPanel = new pivot.ConfigPanel({
                width:300,
                margins:'5 5 5 5',
                region:'west',
                record:pivot.SaleRecord,

                aggregateDimensions:pivotGrid.aggregate,
                leftAxisDimensions:pivotGrid.leftAxis,
                topAxisDimensions:pivotGrid.topAxis,
                enableGrouping:pivotGrid.enableGrouping,
                enableSummary:true,

                listeners:{
                    update:function (config) {
                        pivotGrid.leftAxis = config.leftDimensions;
                        pivotGrid.topAxis = config.topDimensions;
                        pivotGrid.aggregate = config.aggregateDimensions;
                        pivotGrid.enableGrouping = config.enableGrouping;
                        if (config.enableSummary) {
                            featureSummary.enable();
                            if (pivotGrid.enableLocking) {
                                pivotGrid.view.normalView.features[0].enable();
                                pivotGrid.view.lockedView.features[0].enable();
                            }
                        } else {
                            featureSummary.disable();
                            if (pivotGrid.enableLocking) {
                                pivotGrid.view.normalView.features[0].disable();
                                pivotGrid.view.lockedView.features[0].disable();
                            }
                        }

                        pivotGrid.refresh();
                    }
                }
            });

            var viewport = new Ext.Viewport({
                layout:'fit',
                items:{
                    border:false,
                    //title:'mzPivotGrid configurator',
                    layout:'border',
                    items:[
                        configPanel,
                        pivotGrid
                    ]
                }
            });
        }
    });
}
