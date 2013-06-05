/*!
 * Ext JS Library 3.4.0
 * Copyright(c) 2006-2011 Sencha Inc.
 * licensing@sencha.com
 * http://www.sencha.com/license
 */
Ext.ns('pivot');

Ext.Ajax.timeout = 90000;
Ext.Ajax.on('requestexception', function (conn, response, options) {
    if (response.status === 302) {
        document.location = 'login.html';
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
});

function makePivot() {

    //window.gridData = result;
    var gridCols = [
        {name:'date', header:"Date", dataIndex:'date', type:'string'},
        {name:'month', header:"Month", dataIndex:'month', type:'string'},
        {name:'Nobel-Cost', header:"Nobel-Cost", dataIndex:'Nobel-Cost', type:'float'},
        {name:'Nobel-Minutes', header:"Nobel-Minutes", dataIndex:'Nobel-Minutes', type:'int'},
        {name:'RNK-Minutes', header:"RNK-Minutes", dataIndex:'RNK-Minutes', type:'int'},
        {name:'RNK-Total', header:"RNK-Total", dataIndex:'RNK-Total', type:'float'},
        {name:'IDT-minutes', header:"IDT-minutes", dataIndex:'IDT-minutes', type:'int'},
        {name:'IDT-spend', header:"IDT-spend", dataIndex:'IDT-spend', type:'float'},
        {name:'Total-Minutes', header:"Total-Minutes", dataIndex:'Total-Minutes', type:'float'},
        {name:'Total-Cost', header:"Total-Cost", dataIndex:'Total-Cost', type:'float'},
        {name:'Charges', header:"Charges", dataIndex:'Charges', type:'float'},
        {name:'Revenues', header:"Revenues", dataIndex:'Revenues', type:'float'}
    ];

    Ext.define('pivot.SaleRecord', {
        extend:'Ext.data.Model',
        fields:gridCols
    });

    var myStore = new Ext.data.Store({
        autoLoad:true,
        model:'pivot.SaleRecord',
        proxy:{
            type:'ajax',
            url:'data.php',
            reader:{
                type:'json',
                root:'data'
            }
        }
    });

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
            /*exportButton,*/
            {
                xtype:'button',
                text:'Export',
                handler:function () {
                    var ewin = Ext.create("Ext.window.Window", {
                        title:'Export as',
                        layout:{
                            type:'table',
                            columns:2
                        },
                        items:[
                            {
                                xtype:'button',
                                text:'as CSV',
                                handler:function () {

                                }
                            },
                            {
                                xtype:'button',
                                text:'as XLS',
                                handler:function () {

                                }
                            }
                        ]
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

    var d = {"leftDimensions":[
        {"dataIndex":"month", "direction":"desc", "header":"", "width":100},
        {"dataIndex":"date", "direction":"desc", "header":"", "width":70}
    ], "topDimensions":[
        {"dataIndex":"id", "direction":"", "header":"", "width":0}
    ], "aggregateDimensions":[
        {"measure":"Nobel-Cost", "header":"Nobel Cost", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"Nobel-Minutes", "header":"Nobel Minutes", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"RNK-Minutes", "header":"RNK Minutes", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"RNK-Total", "header":"RNK Total", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"IDT-minutes", "header":"IDT Minutes", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"IDT-spend", "header":"IDT Spend", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"Total-Minutes", "header":"Total Minutes", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"Total-Cost", "header":"Total Cost", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"Charges", "header":"Charges", "aggregator":'sum', "renderer":"", "width":75, "align":""},
        {"measure":"Revenues", "header":"Revenues", "aggregator":'sum', "renderer":"", "width":75, "align":""}
    ], "enableGrouping":true, "enableSummary":true};


    configPanel.leftAxisGrid.store.loadData(d.leftDimensions);
    configPanel.topAxisGrid.store.loadData(d.topDimensions);
    configPanel.aggregateGrid.store.loadData(d.aggregateDimensions);
    configPanel.down('[name=chkGrouping]').setValue(d.enableGrouping);
    configPanel.down('[name=chkSummary]').setValue(d.enableSummary);
    configPanel.fireEvent("update", d);

}
