"use strict";this.default_windowbootstrap=this.default_windowbootstrap||{};(function(_){var window=this;
try{
var aa,ba,ca;aa="function"==typeof Object.defineProperties?Object.defineProperty:function(a,b,c){a!=Array.prototype&&a!=Object.prototype&&(a[b]=c.value)};ba="undefined"!=typeof window&&window===this?this:"undefined"!=typeof global&&null!=global?global:this;ca=function(a,b){if(b){var c=ba;a=a.split(".");for(var d=0;d<a.length-1;d++){var e=a[d];e in c||(c[e]={});c=c[e]}a=a[a.length-1];d=c[a];b=b(d);b!=d&&null!=b&&aa(c,a,{configurable:!0,writable:!0,value:b})}};
ca("Object.is",function(a){return a?a:function(b,c){return b===c?0!==b||1/b===1/c:b!==b&&c!==c}});ca("Array.prototype.includes",function(a){return a?a:function(b,c){var d=this;d instanceof String&&(d=String(d));var e=d.length;c=c||0;for(0>c&&(c=Math.max(c+e,0));c<e;c++){var f=d[c];if(f===b||Object.is(f,b))return!0}return!1}});_.da=_.da||{};_.m=this;_.ea="closure_uid_"+(1E9*Math.random()>>>0);_.ha=Date.now||function(){return+new Date};

}catch(e){_._DumpException(e)}
try{
_.Nf="https://support.google.com/chrome/answer/185277?hl="+chrome.i18n.getMessage("@@ui_locale");chrome.i18n.getMessage("@@ui_locale");_.Of="https://support.google.com/hangouts/answer/6127720?hl="+chrome.i18n.getMessage("@@ui_locale");
}catch(e){_._DumpException(e)}
try{
location.search&&window.addEventListener("load",function(){chrome.runtime.getBackgroundPage(function(a){a.__onExtWindowLoad(window)})});
}catch(e){_._DumpException(e)}
}).call(this,this.default_windowbootstrap);
// Google Inc.
