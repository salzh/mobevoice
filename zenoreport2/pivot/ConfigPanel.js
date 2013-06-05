Ext.define('pivot.ConfigPanel', {
    extend:'Ext.panel.Panel',
    alias:'widget.pivotconfig',
    id:'pivotConfigPanel',
    title:'Configure',
    layout:{
        type:'vbox',
        align:'stretch'
    },
    /**
     * @cfg {Ext.data.Record} record The Ext.data.Record to extract the field list from. Required
     */

    initComponent:function () {
        var fields = this.getRecordFields();

        this.form = new Ext.Container({
            layout:'column',
            style:'padding: 7px',
            items:[
                {
                    xtype:'checkbox',
                    fieldLabel:'Enable summary',
                    ref:'/chkSummary',
                    name:'chkSummary',
                    checked:this.enableSummary
                },
                {
                    xtype:'checkbox',
                    fieldLabel:'Enable grouping',
                    ref:'/chkGrouping',
                    name:'chkGrouping',
                    checked:this.enableGrouping,
                    margin:'0 5 5'
                }
            ]
        });

        this.aggregateGrid = new pivot.AggGrid({
            title:'Aggregates',
            fields:fields,
            id:'pivotAggGrid',
            dimensionData:this.aggregateDimensions || [],
            hasWidthField:true
        });

        /**
         * @property leftAxisGrid
         * @type pivot.AxisGrid
         */
        this.leftAxisGrid = new pivot.AxisGrid({
            title:'Left Axis',
            fields:fields,
            id:'pivotLeftAxis',
            dimensionData:this.leftAxisDimensions || [],
            hasWidthField:true
        });

        /**
         * @property topAxisGrid
         * @type pivot.AxisGrid
         */
        this.topAxisGrid = new pivot.AxisGrid({
            title:'Top Axis',
            fields:fields,
            id:'pivotTopAxis',
            dimensionData:this.topAxisDimensions || []
        });

        Ext.applyIf(this, {
            items:[
                this.form,
                this.aggregateGrid,
                this.topAxisGrid,
                this.leftAxisGrid
            ],
            fbar:{
                buttonAlign:'left',
                items:[
                    {
                        text:'Load Saved Pivot',
                        id:'loadSavedPivot',
                        handler:function () {
                            Ext.define("pivotModel", {
                                extend:'Ext.data.Model',
                                fields:[
                                    {name:'name', type:'string'},
                                    {name:'id', type:'int'}
                                ]
                            });
                            var store = Ext.create("Ext.data.Store", {
                                model:'pivotModel',
                                proxy:{
                                    type:'ajax',
                                    url:'database.php?action=getPivots',
                                    extraParams:{
                                        sql:window.gridData.sql
                                    },
                                    reader:{
                                        type:'json',
                                        root:'queries'
                                    }
                                },
                                listeners:{
                                    load:function () {
                                        if (window.first) {
                                            return;
                                        }
                                        window.first = 1;
                                        console.log(Ext.getCmp("chosenPivot").store.data.items.length);
                                        if (Ext.getCmp("chosenPivot").store.data.items.length == 1) {
                                            Ext.getCmp("chosenPivot").setValue(Ext.getCmp("chosenPivot").store.data.items[0]);
                                            Ext.getCmp("LoadPivot").handler();
                                        }
                                    }
                                }
                            });

                            var win = Ext.create("Ext.window.Window", {
                                title:'Choose Pivot',
                                items:[
                                    {
                                        xtype:'combo',
                                        store:store,
                                        displayField:'name',
                                        valueField:'id',
                                        id:'chosenPivot',
                                        listeners:{
                                            afterrender:function () {
                                                this.doQuery(this.allQuery, true);
                                                this.expand();
                                            }
                                        }
                                    }
                                ],
                                bbar:[
                                    {
                                        xtype:'tbfill'
                                    },
                                    {
                                        text:'Load Pivot',
                                        id:'LoadPivot',
                                        handler:function () {

                                            var x = Ext.getCmp("chosenPivot").getValue();
                                            window.savedPivot = x;
                                            Ext.Ajax.request({
                                                url:'database.php?action=getPivot&id=' + x,
                                                success:function (d) {
                                                    try {
                                                        d = Ext.JSON.decode(d.responseText);
                                                    } catch (err) {
                                                        Ext.Msg.alert("Error", "Pivot Data not available, This SQL was not Generated using Zenoreport");
                                                    }
                                                    d = Ext.JSON.decode(d.data);
                                                    var configPanel = Ext.getCmp("pivotConfigPanel");

                                                    configPanel.leftAxisGrid.store.loadData(d.pivotData.leftDimensions);
                                                    configPanel.topAxisGrid.store.loadData(d.pivotData.topDimensions);
                                                    configPanel.aggregateGrid.store.loadData(d.pivotData.aggregateDimensions);

                                                    configPanel.down('[name=chkGrouping]').setValue(d.pivotData.enableGrouping);
                                                    configPanel.down('[name=chkSummary]').setValue(d.pivotData.enableSummary);
                                                    configPanel.fireEvent("update", d.pivotData);

                                                }
                                            });
                                            win.destroy();
                                        }
                                    }
                                ]
                            });

                            win.show();
                        },

                        listeners:{
                            afterrender:function () {
                                this.handler();
                            }
                        }
                    },
                    {
                        icon:'shared/icons/fam/add.gif',
                        text:'Save Pivot',
                        handler:function () {
                            Ext.Msg.prompt("Save as", "Please enter a name for this pivot table", function (btn, e) {
                                console.log(arguments);
                                var data = {};
                                data.sql = window.gridData.sql;
                                data.columnsData = window.gridData.columnsData;

                                if (!window.pivotData) {
                                    Ext.Msg.alert("No Data", "Please update the Pivot atleast Once");
                                    return;
                                }

                                window.pivotData.aggregateDimensions.forEach(function (e1) {
                                    if (e1.aggregator)
                                        e1.aggregator = e1.aggregator.type
                                });
                                data.pivotData = window.pivotData;

                                Ext.Ajax.request({
                                    url:'database.php?action=savepivot',
                                    params:{
                                        name:e,
                                        data:Ext.JSON.encode(data)
                                    },
                                    success:function (d) {
                                        if (d.responseText == "success") {
                                            Ext.Msg.alert("Saved", "Pivot '" + e + "' was saved");
                                        } else {
                                            Ext.Msg.alert("Error", "Some Error occured while saving\n" + d.responseText);
                                        }
                                    }
                                });
                            });
                        }
                    },
                    {
                        icon:'shared/icons/fam/accept.png',
                        text:'Update',
                        scope:this,
                        handler:this.updateGrid
                    }
                ]
            }
        });

        this.callParent(arguments);
    },

    /**
     * @private
     * Retrieves the configured axis dimensions for the top and left grids and updates the PivotGrid accordingly
     */
    updateGrid:function () {
        var leftDimensions = [],
            topDimensions = [],
            aggregateDimensions = [],
            leftGridItems = this.leftAxisGrid.store.data.items,
            topGridItems = this.topAxisGrid.store.data.items,
            aggregateGrid = this.aggregateGrid.store.data.items,
            i;

        for (i = 0; i < leftGridItems.length; i++) {
            leftDimensions.push(leftGridItems[i].data);
        }

        for (i = 0; i < topGridItems.length; i++) {
            topDimensions.push(topGridItems[i].data);
        }

        for (i = 0; i < aggregateGrid.length; i++) {
            aggregateDimensions.push(aggregateGrid[i].data);
        }

        window.pivotData = {
            leftDimensions:leftDimensions,
            topDimensions:topDimensions,
            aggregateDimensions:aggregateDimensions,
            enableGrouping:this.down('[name=chkGrouping]').getValue(),
            enableSummary:this.down('[name=chkSummary]').getValue()
        };
        this.fireEvent('update', pivotData);
    },

    /**
     * Extracts the field names from the configured record
     * @return {Array} The set of Record fields
     */
    getRecordFields:function () {
        window.x = this.record.prototype.fields;
        return Ext.pluck(this.record.prototype.fields.items, 'name');
    }

});

