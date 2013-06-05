/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 1:33 AM
 * To change this template use File | Settings | File Templates.
 */
//Ext.ns("Zenoreport");

Ext.define("Zenoreport.Function", {
    requires:[
        'Zenoreport.view.andOrCombo'
    ],
    singleton:true,
    getTables:function (combobox, value) {
        //window.events.push( ["getTables", arguments] );
        var proxy = {
            type:'ajax',
            url:'database.php?action=getTables&schema=' + value,
            reader:{
                type:'json',
                root:'tables'
            }
        };
        var store = Ext.getCmp("tableGrid").getStore();
        store.setProxy(proxy);
        Ext.getCmp("tableGrid").getStore().load();
        Ext.getCmp("filterTables").focus(true, 100);
    },
    addTable:function (gride, item) {
        //window.events.push( ["addTable", arguments] );
        Ext.define('Table', {
            extend:'Ext.data.Model',
            fields:[
                {name:'ColumnName', type:'string'},
                {
                    name:'Selected',
                    type:'bool'
                },
                {
                    name:'TableName', type:'string'
                },
                {
                    name:'Type', type:'string'
                }
            ],
            set:function (column, value) {
                this.callParent(arguments);
                if (column == "Selected" && value) {
                    Zenoreport.Function.addColumn(this);
                } else if (column == "Selected" && !value) {
                    Zenoreport.Function.removeColumn(this);
                }
            }
        });

        var store = Ext.create('Ext.data.Store', {
            model:'Table',
            proxy:{
                type:'ajax',
                url:'database.php?action=getColumns&table=' + item.get('TableName'),
                reader:{
                    type:'json',
                    root:'Columns'
                }
            },
            autoLoad:true
        });
        store.load();
        var winWidth = store.getCount() > 5 ? 150 : 190;
        console.log("width", winWidth);
        var winHeight = store.getCount() > 5 ? 200 : 300;
        var grid = Ext.create("Ext.grid.GridPanel", {
            store:store,
            enableDragDrop:true,
            ddGroup:'depGridDD',
            columns:[
                {header:'Column', dataIndex:'ColumnName'},
                {
                    header:'Selected',
                    dataIndex:'Selected',
                    xtype:'checkcolumn',
                    width:50
                }
            ],
            selModel:{
                selType:'cellmodel'
            },
            listeners:{
                itemdblclick:function (grid, item) {
                    item.set("Selected", !item.get("Selected"));
                },
                destroy:function (win) {
                    this.getStore().each(function (item) {
                        Zenoreport.Function.removeRelations(item);
                        Zenoreport.Function.removeColumn(item);
                    });
                },
                afterRender:function () {
                    grid.dragZone = new Ext.dd.DragZone(grid.getEl(), {

                        //      On receipt of a mousedown event, see if it is within a DataView node.
                        //      Return a drag data object if so.
                        getDragData:function (e) {

                            //          Use the DataView's own itemSelector (a mandatory property) to
                            //          test if the mousedown is within one of the DataView's nodes.
                            var sourceEl = e.getTarget(grid.itemSelector, 10);

                            //          If the mousedown is within a DataView node, clone the node to produce
                            //          a ddel element for use by the drag proxy. Also add application data
                            //          to the returned data object.
                            if (sourceEl && grid.getView().findTargetByEvent(e)) {
                                var d = sourceEl.cloneNode(true);
                                d.id = Ext.id();
                                window.x = grid.getSelectionModel();
                                return {
                                    ddel:d,
                                    sourceEl:sourceEl,
                                    repairXY:Ext.fly(sourceEl).getXY(),
                                    sourceStore:grid.store,
                                    draggedRecord:grid.getView().getRecord(grid.getView().findTargetByEvent(e))
                                }
                            }
                        },

                        //      Provide coordinates for the proxy to slide back to on failed drag.
                        //      This is the original XY coordinates of the draggable element captured
                        //      in the getDragData method.
                        getRepairXY:function () {
                            return this.dragData.repairXY;
                        }
                    });

                    grid.dropZone = new Ext.dd.DropZone(grid.getView().getEl(), {
                        // If the mouse is over a grid row, return that node. This is
                        // provided as the "target" parameter in all "onNodeXXXX" node event handling functions
                        getTargetFromEvent:function (e) {
                            return e.getTarget(grid.getView().rowSelector);
                        },

                        // On entry into a target node, highlight that node.
                        onNodeEnter:function (target, dd, e, data) {
                            Ext.fly(target).addCls('my-row-highlight-class');
                        },

                        // On exit from a target node, unhighlight that node.
                        onNodeOut:function (target, dd, e, data) {
                            Ext.fly(target).removeCls('my-row-highlight-class');
                        },

                        // While over a target node, return the default drop allowed class which
                        // places a "tick" icon into the drag proxy.
                        onNodeOver:function (target, dd, e, data) {
                            return Ext.dd.DropZone.prototype.dropAllowed;
                        },

                        // On node drop we can interrogate the target to find the underlying
                        // application object that is the real target of the dragged data.
                        // In this case, it is a Record in the GridPanel's Store.
                        // We can use the data set up by the DragZone's getDragData method to read
                        // any data we decided to attach in the DragZone's getDragData method.
                        onNodeDrop:function (target, dd, e, data) {
                            var r = grid.getView().getRecord(grid.getView().findTargetByEvent(e));
                            var newRelation = {
                                es:data.draggedRecord.get("TableName"),
                                fs:data.draggedRecord.get("ColumnName"),
                                et:r.get("TableName"),
                                ft:r.get("ColumnName")
                            };
                            relations.push(newRelation);

                            Zenoreport.Function.showRelationWindow();

                            return true;
                        }
                    });
                }
            }
        });
        var win = Ext.create('Ext.window.Window', {
            title:item.get('TableName'),
            //width:winWidth,
            //height:winHeight,
            x:10,
            y:30,
            layout:'fit',
            items:[
                grid
            ]
        });
        var body = Ext.getCmp("zenoreportBody");
        body.add(win);
        win.show();
        win.setSize(winWidth, winHeight);
        //grid.render();

        window.grid = grid;
    },

    addSelect:function (column, criteria) {
        criteria = criteria || {};
        var selectBox = Ext.create('Ext.panel.Panel', {
            layout:'vbox',
            floating:false,
            column:column,
            width:130,
            id:'SelectColumn' + column.id,
            height:220,
            defaults:{
                style:{
                    margin:'0 0 0 0'
                }
            },
            items:[
                {
                    xtype:'textfield',
                    value:criteria.fieldName || column.get("ColumnName")
                },
                {
                    xtype:'textfield'
                },
                {

                    xtype:'textfield',
                    value:column.get("TableName"),
                    readOnly:true
                },
                {
                    xtype:'combobox',
                    store:Ext.create("Ext.data.Store", {
                        fields:['Name', 'Value'],
                        data:[
                            {Name:'Ascending', Value:'ASC'},
                            {Name:'Descending', Value:'DESC'}
                        ],
                        queryMode:'local'
                    }),
                    displayField:'Name',
                    valueField:'Value',
                    width:127,
                },
                {
                    xtype:'checkbox',
                    checked:true
                },
                {
                    xtype:'textfield',
                    value:criteria.criteria || ""
                },
                {
                    xtype:'textfield'
                },
                {
                    xtype:'textfield'
                },
                {
                    xtype:'combobox',
                    width:127,
                    store:Ext.create("Ext.data.Store", {
                        fields:['Name', 'Value'],
                        data:[
                            {Name:'Sum', Value:'sum'},
                            {Name:'Count', Value:'count'},
                            {Name:'Max', Value:'max'},
                            {Name:'Min', Value:'min'},
                            {Name:'Average', Value:'avg'}
                        ],
                        queryMode:'local'
                    }),
                    displayField:'Name',
                    valueField:'Value',
                    value:criteria.aggregate || ""
                },
                {
                    xtype:'checkbox',
                    checked:(column.get("Type") != "int" && window.allgroupby) || criteria.groupby
                },
                {
                    xtype:'hiddenfield',
                    value:column.get("ColumnName")
                }
            ]
        });
        Ext.getCmp("selectedColumns").add(selectBox);

        //selectBox.render();
        var selectColumns;
        if (criteria.aggregate && criteria.aggregate.length > 1) {
            window.allgroupby = true;
            selectColumns = Ext.getCmp("selectedColumns").items;
            for (var i = 1; i < selectColumns.getCount(); i++) {
                if (selectColumns.get(i).column.get("Type") != "int") {
                    selectColumns.get(i).items.get(9).setValue(true);
                }
            }
        } else {
            var nogroupby = false;
            selectColumns = Ext.getCmp("selectedColumns").items;
            for (var i = 1; (!nogroupby) && (i < selectColumns.getCount()); i++) {
                if (selectColumns.get(i).column.get("Type") != "int") {
                    nogroupby = nogroupby || selectColumns.get(i).items.get(9).getValue();
                }
            }
            window.allgroupby = nogroupby;
        }
    },

    addColumn:function (column) {
        var items = [];
        var windowTitle = "Select Criteria";
        var type = column.get("Type");
        var bbar;
        if (type == "datetime") {
            windowTitle = "Select Date Criteria [" + column.get("ColumnName") + "]";
            bbar = [
                {
                    xtype:'tbfill'
                },
                {
                    text:'No Criteria',
                    label:'&nbsp;',
                    handler:function () {
                        Zenoreport.Function.addSelect(column, {});
                        win.destroy();
                    }
                },
                {
                    text:'Dont Add',
                    label:'&nbsp;',
                    handler:function () {
                        column.set("Selected", false);
                        win.destroy();
                    }
                },
                {
                    text:'Okay!',
                    label:'&nbsp;',
                    handler:function () {
                        var reference = Ext.getCmp("fieldReference").getValue() ?
                            "'" + Ext.Date.format(Ext.getCmp("fieldReference").getValue(), "Y-m-d") + "'" : "NOW()";
                        var criteria = {
                            fieldName:Ext.getCmp("fieldName").getValue(),
                            criteria:'>date_add('
                                + reference
                                + ", interval "
                                + Ext.getCmp("fieldIntervalValue").getValue()
                                + " "
                                + Ext.getCmp("fieldInterval").getValue()
                                + ")"
                        };
                        Zenoreport.Function.addSelect(column, criteria);
                        win.destroy();
                    }
                }
            ];
            items.push(
                {
                    xtype:'combo',
                    id:'fieldName',
                    fieldLabel:'Select as',
                    store:Ext.create("Ext.data.Store", {
                        fields:['name', 'value'],
                        data:[
                            {name:'Year', value:'substr( ' + column.get("ColumnName") + ' , 1, 4)'},
                            {name:'Month', value:'substr( ' + column.get("ColumnName") + ' , 1, 7)'},
                            {name:'Day', value:'substr( ' + column.get("ColumnName") + ' , 1, 10)'},
                            {name:'Hour', value:'substr( ' + column.get("ColumnName") + ' , 1, 13)'},
                            {name:'Minute', value:'substr( ' + column.get("ColumnName") + ' , 1, 16)'},
                            {name:'Complete', value:column.get("ColumnName")}
                        ],
                        queryMode:'local'
                    }),
                    displayField:'name',
                    valueField:'value',
                    queryMode:'local',
                    value:column.get("ColumnName")
                },
                {
                    xtype:'container',
                    layout:'hbox',
                    width:250,
                    autoRender:true,
                    items:[
                        {
                            xtype:'textfield',
                            fieldLabel:'Interval',
                            id:'fieldIntervalValue',
                            value:'-7',
                            width:100,
                            fieldStyle:{
                                width:50
                            },
                            labelWidth:45,
                            style:'width: 50px'
                        },
                        {
                            xtype:'combobox',
                            id:'fieldInterval',
                            width:100,
                            store:Ext.create("Ext.data.Store", {
                                fields:['name', 'value'],
                                data:[
                                    {name:'Minutes', value:'minute'},
                                    {name:'Hours', value:'hour'},
                                    {name:'Days', value:'day'},
                                    {name:'Weeks', value:'week'},
                                    {name:'Months', value:'month'},
                                    {name:'Years', value:'year'}
                                ],
                                queryMode:'local',
                                mode:'local'
                            }),
                            queryMode:'local',
                            displayField:'name',
                            valueField:'value',
                            value:'day'
                        }
                    ]
                },
                {
                    xtype:'datefield',
                    fieldLabel:'Since',
                    id:'fieldReference',
                    emptyText:'NOW()',
                    format:'Y-m-d'
                }
            );
        }
        else if (type == "int" || type == "float") {
            windowTitle = "Select Numeric Criteria [" + column.get("ColumnName") + "]";
            var suggestion = "";
            var defaultAggregate = "";
            if (column.get("ColumnName").indexOf("_id") > -1 || column.get("ColumnName") == "id") {
                suggestion = "<br/>If you are counting, select COUNT aggregate. <br/>->Average/SUM would be meaningless.<br/>";
                defaultAggregate = "COUNT";
            } else {
                suggestion = "<br/>Numeric Data can be Summed, <br/>Averaged for meaningful Data.<br/>";
                defaultAggregate = "SUM";
            }
            bbar = [
                {
                    xtype:'tbfill'
                },
                {
                    text:'No Criteria',
                    label:'&nbsp;',
                    handler:function () {
                        Zenoreport.Function.addSelect(column, {});
                        win.destroy();
                    }
                },
                {
                    text:'Dont Add',
                    label:'&nbsp;',
                    handler:function () {
                        column.set("Selected", false);
                        win.destroy();
                    }
                },
                {
                    text:'Okay!',
                    label:'&nbsp;',
                    handler:function () {
                        var name = column.get("ColumnName");
                        if (Ext.getCmp("selectRound").getValue()) {
                            name = "ROUND(" + name + ")";
                        }
                        var criteria = {
                            fieldName:name,
                            aggregate:Ext.getCmp("selectAggregate").getValue()
                        };
                        Zenoreport.Function.addSelect(column, criteria);
                        win.destroy();
                    }
                }
            ];
            items.push(
                {
                    xtype:'label',
                    html:suggestion
                },
                {
                    xtype:'checkbox',
                    fieldLabel:'Round Up Data',
                    checked:defaultAggregate == "SUM",
                    id:'selectRound'
                },
                {
                    xtype:'combo',
                    id:'selectAggregate',
                    store:Ext.create("Ext.data.Store", {
                        fields:[
                            {name:'name', type:'string'},
                            {name:'value', type:'value'}
                        ],
                        data:[
                            {name:'No Aggregation', value:''},
                            {name:'Count Rows', value:'COUNT'},
                            {name:'Sum Values', value:'SUM'},
                            {name:'Get Average', value:'AVG'},
                            {name:'Get MAXIMUM', value:'MAX'},
                            {name:'Get MINIMUM', value:'MIN'}
                        ]
                    }),
                    displayField:'name',
                    valueField:'value',
                    value:defaultAggregate,
                    fieldLabel:'Aggregate'
                }
            );
        }
        else if (type == "string") {
            windowTitle = "Select Text Criteria [" + column.get("ColumnName") + "]";
            bbar = [
                {
                    xtype:'tbfill'
                },
                {
                    text:'+Condition',
                    handler:function () {
                        var xx = Ext.create("Zenoreport.view.MoreStringCondition");
                        var x = Ext.getCmp("moreConditions").add(xx);
                        x.up("window").doComponentLayout();
                    },
                    listeners:{
                        afterrender:function (txt) {
                            txt.up("window").setSize(320);
                        }
                    }
                },
                {
                    text:'No Criteria',
                    label:'&nbsp;',
                    handler:function () {
                        Zenoreport.Function.addSelect(column, {});
                        win.destroy();
                    }
                },
                {
                    text:'Dont Add',
                    label:'&nbsp;',
                    handler:function () {
                        column.set("Selected", false);
                        win.destroy();
                    }
                },
                {
                    text:'Okay!',
                    label:'&nbsp;',
                    handler:function (btn) {
                        window.win = btn.up("window");
                        if (!win.items.get(0)
                            || !win.items.get(0).items.get(0).getValue()
                            || win.items.get(0).items.get(0).getValue().length < 1) {
                            Zenoreport.Function.addSelect(column, criteria);
                            return win.destroy();
                        }
                        var cStr = win.items.get(0).items.get(0).getValue().replace("STR", win.items.get(0).items.get(1).getValue());
                        var moreCondition = win.items.get(1);
                        for (var i = 0; i < moreCondition.items.getCount(); i++) {
                            var moreConditions = moreCondition.items.get(i);
                            if (
                                moreConditions.items.get(1).getValue()
                                    && moreConditions.items.get(2).items.get(0).getValue()
                                    && moreConditions.items.get(2).items.get(1).getValue()
                                ) {
                                cStr += " " + moreConditions.items.get(1).getValue() + " "
                                    + moreConditions.items.get(2).items.get(0).getValue().replace("STR",
                                    moreConditions.items.get(2).items.get(1).getValue()
                                );
                            }
                        }
                        var name = column.get("ColumnName");
                        var criteria = {
                            criteria:cStr
                        };
                        Zenoreport.Function.addSelect(column, criteria);
                        win.destroy();
                    }
                }
            ];
            items.push(
                //{xtype:'stringconditioncombo'},
                Ext.create("Zenoreport.view.StringConditionCombo"),
                {
                    xtype:'container',
                    id:'moreConditions',
                    layout:'auto',
                    items:[]
                }
            );
        }

        var win = Ext.create("Ext.window.Window", {
            title:windowTitle,
            layout:'auto',
            items:items,
            bbar:bbar
        });

        win.show();
    },

    removeRelations:function (column) {
        var tableName = column.get("TableName");
        for (var i = 0; i < relations.length; i++) {
            if (relations[i].es == tableName || relations[i].et == tableName) {
                relations.splice(i, 1);
                i--;
            }
        }
        if (Ext.getCmp("relationWindow")) {
            Ext.getCmp("relationWindow").items.get(0).getStore().loadData(relations);
        }
    },

    removeColumn:function (column) {
        var id = 'SelectColumn' + column.id;
        if (Ext.getCmp(id)) {
            Ext.getCmp(id).destroy();
        }
    },

    addOnce:function () {
        var selectBox = Ext.create('Ext.panel.Panel', {
            layout:'vbox',
            floating:false,
            width:100,
            height:220,
            defaults:{
                xtype:'displayfield'
            },
            items:[
                {fieldLabel:'Field'},
                {fieldLabel:'Alias'},
                {fieldLabel:'Table'},
                {fieldLabel:'Sort'},
                {fieldLabel:'Display'},
                {fieldLabel:'Criteria'},
                {fieldLabel:'Or'},
                {fieldLabel:'Or'},
                {fieldLabel:'Aggregate'},
                {fieldLabel:'GroupBy'}
            ]
        });
        Ext.getCmp("selectedColumns").add(selectBox);
    },

    showRelationWindow:function () {
        var win = Ext.getCmp("relationWindow");
        if (win) {
            win.items.get(0).getStore().loadData(relations);
            win.show();
            return;
        }
        win = Ext.create("Zenoreport.view.Relation");
        win.show();
        win.alignTo(Ext.getBody(), "tr-tr", [-10, 10]);
    }

});