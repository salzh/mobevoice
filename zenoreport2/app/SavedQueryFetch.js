/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 10/22/12
 * Time: 11:44 PM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.SavedQueryFetch", {
    singleton:true,
    getSavedQuery:function (name, limit, callBack) {

        limit = limit || 100;

        Ext.Ajax.request({
            url:"database.php?action=getSavedQuery&name=" + name + "&limit=" + limit,
            success:function (data) {
                if (data.responseText == "success") {
                    callBack()
                } else {
                    try {
                        var result = Ext.JSON.decode(data.responseText);
                        if (result.result == "getvariables") {
                            var variables = result.variables;
                            if (variables.length > 0) {
                                var items = [];
                                for (var i = 0; i < variables.length; i++) {
                                    var name = variables[i];
                                    items.push({
                                        xtype:'textfield',
                                        fieldLabel:name
                                    });
                                }

                                var win = Ext.create("Ext.window.Window", {
                                    title:'Enter Variables',
                                    layout:'anchor',
                                    items:items,
                                    bbar:[
                                        {xtype:'tbfill'},
                                        {
                                            xtype:'button',
                                            text:'Query',
                                            handler:function () {
                                                win.mask("Loading");
                                                var returndata = [];
                                                for (var i = 0; i < win.items.items.length; i++) {
                                                    var item = win.items.items[i];
                                                    returndata.push({
                                                        name:item.fieldLabel,
                                                        value:item.getValue()
                                                    });
                                                }
                                                Ext.Ajax.request({
                                                    url:'database.php?action=setSavedParams',
                                                    params:{
                                                        data:Ext.JSON.encode(returndata)
                                                    },
                                                    success:function (data1) {
                                                        win.unmask();
                                                        console.log(data1);
                                                        data = Ext.JSON.decode(data1.responseText);
                                                        if (data.result == "success") {
                                                            win.destroy();
                                                            callBack();
                                                        } else {
                                                            Ext.Msg.alert("Some Error Occured\n" + data1.responseText);
                                                        }
                                                    }
                                                })
                                            }
                                        }
                                    ]
                                });
                                window.win = win;
                                win.show();
                            } else {
                                callBack();
                            }
                        }
                    } catch (e) {
                        Ext.Msg.alert("Error", "Some Error Occured\n" + data.responseText);
                    }
                }
            }
        });
    }
});