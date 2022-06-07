(function(){"use strict";var e={3783:function(e,t,n){n(6992),n(8674),n(9601),n(7727);var o=n(144),r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-main",[n("router-view")],1)},i=[],u={name:"App",data:function(){return{}}},a=u,c=n(1001),s=n(3453),l=n.n(s),f=n(7877),d=(0,c.Z)(a,r,i,!1,null,null,null),v=d.exports;l()(d,{VMain:f.Z});var p=n(5205);(0,p.z)("".concat("/static/","service-worker.js"),{ready:function(){console.log("App is being served from cache by a service worker.\nFor more details, visit https://goo.gl/AFskqB")},registered:function(){console.log("Service worker has been registered.")},cached:function(){console.log("Content has been cached for offline use.")},updatefound:function(){console.log("New content is downloading.")},updated:function(){console.log("New content is available; please refresh.")},offline:function(){console.log("No internet connection found. App is running in offline mode.")},error:function(e){console.error("Error during service worker registration:",e)}});n(1539),n(8783),n(3948);var m=n(8345),h=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("hello-world")},g=[],b=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-card",{staticClass:"mx-auto overflow-hidden",attrs:{height:"400"}},[n("v-app-bar",{attrs:{color:"deep-purple",dark:""}},[n("v-app-bar-nav-icon",{on:{click:function(t){e.drawer=!0}}}),n("v-toolbar-title",[e._v("Title")])],1),n("v-navigation-drawer",{attrs:{absolute:"",temporary:""},model:{value:e.drawer,callback:function(t){e.drawer=t},expression:"drawer"}},[n("v-list",{attrs:{nav:"",dense:""}},[n("v-list-item-group",{attrs:{"active-class":"deep-purple--text text--accent-4"},model:{value:e.group,callback:function(t){e.group=t},expression:"group"}},[n("v-list-item",[n("v-list-item-icon",[n("v-icon",[e._v("mdi-home")])],1),n("v-list-item-title",[e._v("Home")])],1),n("v-list-item",[n("v-list-item-icon",[n("v-icon",[e._v("mdi-account")])],1),n("v-list-item-title",[e._v("Account")])],1)],1)],1)],1)],1)},y=[],w={name:"HelloWorld",data:function(){return{drawer:!1,ecosystem:[{text:"vuetify-loader",href:"https://github.com/vuetifyjs/vuetify-loader"},{text:"github",href:"https://github.com/vuetifyjs/vuetify"},{text:"awesome-vuetify",href:"https://github.com/vuetifyjs/awesome-vuetify"}],importantLinks:[{text:"Documentation",href:"https://vuetifyjs.com"},{text:"Chat",href:"https://community.vuetifyjs.com"},{text:"Made with Vuetify",href:"https://madewithvuejs.com/vuetify"},{text:"Twitter",href:"https://twitter.com/vuetifyjs"},{text:"Articles",href:"https://medium.com/vuetify"}],whatsNext:[{text:"Explore components",href:"https://vuetifyjs.com/components/api-explorer"},{text:"Select a layout",href:"https://vuetifyjs.com/getting-started/pre-made-layouts"},{text:"Frequently Asked Questions",href:"https://vuetifyjs.com/getting-started/frequently-asked-questions"}]}}},x=w,k=n(8320),Z=n(4542),j=n(26),V=n(6428),_=n(6816),O=n(7620),A=n(6651),T=n(459),E=n(3901),C=n(3120),N=n(7921),L=(0,c.Z)(x,b,y,!1,null,null,null),P=L.exports;l()(L,{VAppBar:k.Z,VAppBarNavIcon:Z.Z,VCard:j.Z,VIcon:V.Z,VList:_.Z,VListItem:O.Z,VListItemGroup:A.Z,VListItemIcon:T.Z,VListItemTitle:E.V9,VNavigationDrawer:C.Z,VToolbarTitle:N.qW});var S={name:"HomeView",components:{HelloWorld:P}},I=S,q=(0,c.Z)(I,h,g,!1,null,null,null),F=q.exports;o.Z.use(m.Z);var M=[{path:"/",name:"home",component:F},{path:"/about",name:"about",component:function(){return n.e(443).then(n.bind(n,1872))}}],B=new m.Z({mode:"history",base:"/static/",routes:M}),H=B,$=n(629);o.Z.use($.ZP);var W=new $.ZP.Store({state:{},getters:{},mutations:{},actions:{},modules:{}}),D=n(5591);o.Z.use(D.Z);var z=new D.Z({theme:{themes:{light:{primary:"#00bcd4",accent:"#ff9800"}}}});o.Z.config.productionTip=!1,new o.Z({router:H,store:W,vuetify:z,render:function(e){return e(v)}}).$mount("#app")}},t={};function n(o){var r=t[o];if(void 0!==r)return r.exports;var i=t[o]={exports:{}};return e[o](i,i.exports,n),i.exports}n.m=e,function(){var e=[];n.O=function(t,o,r,i){if(!o){var u=1/0;for(l=0;l<e.length;l++){o=e[l][0],r=e[l][1],i=e[l][2];for(var a=!0,c=0;c<o.length;c++)(!1&i||u>=i)&&Object.keys(n.O).every((function(e){return n.O[e](o[c])}))?o.splice(c--,1):(a=!1,i<u&&(u=i));if(a){e.splice(l--,1);var s=r();void 0!==s&&(t=s)}}return t}i=i||0;for(var l=e.length;l>0&&e[l-1][2]>i;l--)e[l]=e[l-1];e[l]=[o,r,i]}}(),function(){n.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(t,{a:t}),t}}(),function(){n.d=function(e,t){for(var o in t)n.o(t,o)&&!n.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:t[o]})}}(),function(){n.f={},n.e=function(e){return Promise.all(Object.keys(n.f).reduce((function(t,o){return n.f[o](e,t),t}),[]))}}(),function(){n.u=function(e){return"js/about-legacy.6ae00a5a.js"}}(),function(){n.miniCssF=function(e){}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={},t="frontend:";n.l=function(o,r,i,u){if(e[o])e[o].push(r);else{var a,c;if(void 0!==i)for(var s=document.getElementsByTagName("script"),l=0;l<s.length;l++){var f=s[l];if(f.getAttribute("src")==o||f.getAttribute("data-webpack")==t+i){a=f;break}}a||(c=!0,a=document.createElement("script"),a.charset="utf-8",a.timeout=120,n.nc&&a.setAttribute("nonce",n.nc),a.setAttribute("data-webpack",t+i),a.src=o),e[o]=[r];var d=function(t,n){a.onerror=a.onload=null,clearTimeout(v);var r=e[o];if(delete e[o],a.parentNode&&a.parentNode.removeChild(a),r&&r.forEach((function(e){return e(n)})),t)return t(n)},v=setTimeout(d.bind(null,void 0,{type:"timeout",target:a}),12e4);a.onerror=d.bind(null,a.onerror),a.onload=d.bind(null,a.onload),c&&document.head.appendChild(a)}}}(),function(){n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){n.p="/static/"}(),function(){var e={143:0};n.f.j=function(t,o){var r=n.o(e,t)?e[t]:void 0;if(0!==r)if(r)o.push(r[2]);else{var i=new Promise((function(n,o){r=e[t]=[n,o]}));o.push(r[2]=i);var u=n.p+n.u(t),a=new Error,c=function(o){if(n.o(e,t)&&(r=e[t],0!==r&&(e[t]=void 0),r)){var i=o&&("load"===o.type?"missing":o.type),u=o&&o.target&&o.target.src;a.message="Loading chunk "+t+" failed.\n("+i+": "+u+")",a.name="ChunkLoadError",a.type=i,a.request=u,r[1](a)}};n.l(u,c,"chunk-"+t,t)}},n.O.j=function(t){return 0===e[t]};var t=function(t,o){var r,i,u=o[0],a=o[1],c=o[2],s=0;if(u.some((function(t){return 0!==e[t]}))){for(r in a)n.o(a,r)&&(n.m[r]=a[r]);if(c)var l=c(n)}for(t&&t(o);s<u.length;s++)i=u[s],n.o(e,i)&&e[i]&&e[i][0](),e[i]=0;return n.O(l)},o=self["webpackChunkfrontend"]=self["webpackChunkfrontend"]||[];o.forEach(t.bind(null,0)),o.push=t.bind(null,o.push.bind(o))}();var o=n.O(void 0,[998],(function(){return n(3783)}));o=n.O(o)})();
//# sourceMappingURL=app-legacy.3c03477e.js.map