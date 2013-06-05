/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 2:33 PM
 * To change this template use File | Settings | File Templates.
 */


Ext.define("Zenoreport.view.Relation", {
    extend:'Ext.window.Window',
    title:'Relations',
    layout:'fit',
    id:'relationWindow',
    width:414,
    height:300,
    y:0,
    items:[
        {
            xtype:'grid',
            store:Ext.create('Zenoreport.store.Relation'),
            columns:[
                {header:'From Table', dataIndex:'es'},
                {header:'From Column', dataIndex:'fs'},
                {header:'To Table', dataIndex:'et'},
                {header:'To Column', dataIndex:'ft'}
            ]
        }
    ],
    dockedItems:[
        {
            xtype:'toolbar',
            dock:'bottom',
            items:[
                {
                    text:'Remove',
                    handler:function () {
                        win.items.get(0).getView().selModel.selected.items.forEach(function (rel) {
                            store.remove(rel);
                        });
                        relations = [];
                        Ext.getCmp("relationWindow").items.get(0).getStore().each(function (e) {
                            relations.push(e.data);
                        });
                    }
                },
                {
                    text:'Remove All',
                    handler:function () {
                        win.destroy();
                        relations = [];
                        Zenoreport.Function.showRelationWindow();
                    }
                }
            ]
        }
    ]
});