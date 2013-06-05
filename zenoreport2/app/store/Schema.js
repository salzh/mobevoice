/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 6:13 AM
 * To change this template use File | Settings | File Templates.
 */


Ext.define('Zenoreport.store.Schema', {
    extend:'Ext.data.Store',
    requires:[
        'Zenoreport.model.Schema'
    ],
    //autoLoad:true,
    constructor:function (cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId:'Zenoreport.model.Schema',
            model:'Zenoreport.model.Schema'
        }, cfg)]);
    }
});