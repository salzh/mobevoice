/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 4:04 AM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.ZenoChart", {
    extend:'Ext.window.Window',
    title:'Zeno Chart',
    id:'chartStartWindow',
    width:400,
    layout:{
        type:'table',
        columns:4
    },
    defaults:{
        height:100,
        width:100,
        handler:function () {
            var type = this.text.replace(" ", "");
            startCharting(type);
            Ext.getCmp("chartStartWindow").destroy();
        },
        xtype:'button'
    },
    items:[
        {text:'Area Chart'},
        {text:'Bar Chart'},
        {text:'Bubble Chart'},
        {text:'Candlestick Chart'},
        {text:'Column Chart'},
        {text:'Gauge Chart'},
        {text:'Line Chart'},
        {text:'Pie Chart'},
        {text:'Table Chart'}
    ]
});

function startCharting(type) {
    var d = [];

    if (!window.gridData || !window.gridData.columnsData || window.gridData.data.length < 0) {
        Ext.Msg.alert({
            title:'No Data',
            msg:'No Data to make report',
            buttons:Ext.Msg.OK,
            icon:Ext.Msg.ERROR
        });
        return;
    }

    window.gridData.columnsData.forEach(function (col) {
        d.push({Colname:col.name, value:col.name, type:col.type == 'int' ? col.type : 'string'});
    });
    console.log(d);
    var columnStore = Ext.create("Ext.data.Store", {
        fields:['Colname', 'value'],
        data:d,
        queryMode:'local'
    });


    var win = Ext.create("Ext.window.Window", {
        title:'Chart Configurations',
        layout:'vbox',
        width:270,
        height:140,
        items:[
            {
                xtype:'combo',
                store:columnStore,
                id:'xaxis',
                displayField:'Colname',
                valueField:'value',
                queryMode:'local',
                fieldLabel:'X Axis Field'
            },
            {
                xtype:'combo',
                fieldLabel:'Y Axis Fields',
                id:'yaxis',
                store:columnStore,
                displayField:'Colname',
                valueField:'value',
                queryMode:'local',
                multiSelect:true
            }
        ],
        bbar:[
            {xtype:'tbfill'},
            {
                xtype:'button',
                text:'Continue',
                listeners:{
                    click:function () {
                        var xAxis = Ext.getCmp("xaxis").getValue();
                        var yAxis = Ext.getCmp("yaxis").getValue();
                        win.removeAll();
                        win.setSize(600, 400);
                        var columns = [];
                        columns.push(xAxis);
                        for (var i = 0; i < yAxis.length; i++) {
                            columns.push(yAxis[i]);
                        }
                        var data = [];
                        data.push(columns);

                        for (i = 0; i < window.store.getCount(); i++) {
                            var d = [];
                            for (var j = 0; j < columns.length; j++) {
                                d.push(window.store.getAt(i).get(columns[j]));
                            }
                            data.push(d);
                        }
                        console.log(data);
                        window.gdata = google.visualization.arrayToDataTable(data);

                        window.options = {
                            title:'Chart',
                            hAxis:{title:columns[0], titleTextStyle:{color:'red'}}
                        };
                        window.chart = new google.visualization[type](win.body.dom);
                        chart.draw(gdata, options);
                        win.on({
                            resize:{
                                fn:function () {
                                    window.chart.draw(window.gdata, window.options);
                                }
                            }
                        })
                    }
                }
            }
        ]
    });
    win.show();


}