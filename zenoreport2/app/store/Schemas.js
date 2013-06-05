/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 6:13 AM
 * To change this template use File | Settings | File Templates.
 */


Ext.define('Zenoreport.store.Schemas', {
    extend:'Ext.data.Store',
    requires:[
        'Zenoreport.model.Schemas'
    ],
    autoLoad:true,
    constructor:function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId:'Schemas',
            model:'Zenoreport.model.Schemas',
            proxy:{
                type:'ajax',
                url:'database.php?action=getSchemas',
                reader:{
                    type:'json',
                    root:'schemas'
                }
            }
        }, cfg)]);
    }
});