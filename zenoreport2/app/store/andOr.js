/**
 * Created with JetBrains PhpStorm.
 * User: Pheonix
 * Date: 9/29/12
 * Time: 1:53 PM
 * To change this template use File | Settings | File Templates.
 */

Ext.define("Zenoreport.store.andOr", {
    extend:'Ext.data.Store',
    autoLoad:true,
    constructor:function (cfg) {
        cfg = cfg || {};
        this.callParent([Ext.apply({
            storeId: 'andOr',
            fields:['name', 'vale'],
            data:[
                {name:'AND', value:'AND'},
                {name:'OR', value:'OR'}
            ],
            queryMode:'local'
        }, cfg)]);
    }
});