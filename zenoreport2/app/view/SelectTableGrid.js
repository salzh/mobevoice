/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 2:57 AM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.view.SelectTableGrid", {
    extend:'Ext.window.Window',
    title:'Select Schema',
    id:'tablesWindow',
    height:300,
    width:215,
    closeAction:'destroy',
    layout:'border',
    items:[
        {
            region:'north',
            xtype:'container',
            height:50,
            layout:'vbox',
            defaults:{
                width:200
            },
            items:[
                {
                    xtype:'combo',
                    id:'schemaCombo',
                    emptyText:'Select a Schema',
                    store: 'Schemas',
                    displayField:'SchemaName',
                    valueField:'SchemaName',
                    listeners:{
                        change:Zenoreport.Function.getTables,
                        afterrender:function () {
                            this.doQuery(this.allQuery, true);
                            this.expand();
                        }
                    }
                },
                {
                    xtype:'textfield',
                    id:'filterTables',
                    emptyText:'Filter Table By Name',
                    listeners:{
                        change:function (textfield, value) {
                            var store = Ext.getCmp("tableGrid").getStore();
                            store.clearFilter();
                            if (!value || value.length < 1)return;
                            var regex = new RegExp(value);
                            store.filter("TableName", regex);
                        }
                    }
                }
            ]
        },
        {
            region:'center',
            xtype:'grid',
            id:'tableGrid',
            multiSelect:true,
            width:200,
            store: 'Schema',
            columns:[
                {header:'Table Name', dataIndex:'TableName', width:200}
            ],
            listeners:{
                itemdblclick:Zenoreport.Function.addTable
            }
        },
        {
            region:'south',
            xtype:'toolbar',
            items:[
                {xtype:'tbfill'},
                {
                    xtype:'button',
                    layout:'fit',
                    text:'Add Selected',
                    handler:function () {
                        var grid = Ext.getCmp("tableGrid");
                        var selModel = grid.getSelectionModel();
                        selModel.selected.items.forEach(function (item) {
                            Zenoreport.Function.addTable(grid, item);
                        });
                        selModel.selectRange(-1, 0, false);
                    }
                },
                {
                    xtype:'button',
                    layout:'fit',
                    text:'Close',
                    handler:function () {
                        Ext.getCmp("tablesWindow").destroy();
                    }
                }
            ]
        }
    ]
});