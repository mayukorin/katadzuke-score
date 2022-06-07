(function(){"use strict";var e={3783:function(e,t,n){var r=n(144),o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-main",[n("router-view")],1)},i=[],a={name:"App",data:()=>({})},u=a,s=n(1001),c=n(3453),l=n.n(c),f=n(7877),d=(0,s.Z)(u,o,i,!1,null,null,null),v=d.exports;l()(d,{VMain:f.Z});var p=n(5205);(0,p.z)("/static/service-worker.js",{ready(){console.log("App is being served from cache by a service worker.\nFor more details, visit https://goo.gl/AFskqB")},registered(){console.log("Service worker has been registered.")},cached(){console.log("Content has been cached for offline use.")},updatefound(){console.log("New content is downloading.")},updated(){console.log("New content is available; please refresh.")},offline(){console.log("No internet connection found. App is running in offline mode.")},error(e){console.error("Error during service worker registration:",e)}});var m=n(8345),h=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("hello-world")},g=[],b=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("v-card",{staticClass:"mx-auto overflow-hidden",attrs:{height:"400"}},[n("v-app-bar",{attrs:{color:"deep-purple",dark:""}},[n("v-app-bar-nav-icon",{on:{click:function(t){e.drawer=!0}}}),n("v-toolbar-title",[e._v("Title")])],1),n("v-navigation-drawer",{attrs:{absolute:"",temporary:""},model:{value:e.drawer,callback:function(t){e.drawer=t},expression:"drawer"}},[n("v-list",{attrs:{nav:"",dense:""}},[n("v-list-item-group",{attrs:{"active-class":"deep-purple--text text--accent-4"},model:{value:e.group,callback:function(t){e.group=t},expression:"group"}},[n("v-list-item",[n("v-list-item-icon",[n("v-icon",[e._v("mdi-home")])],1),n("v-list-item-title",[e._v("Home")])],1),n("v-list-item",[n("v-list-item-icon",[n("v-icon",[e._v("mdi-account")])],1),n("v-list-item-title",[e._v("Account")])],1)],1)],1)],1)],1)},y=[],w={name:"HelloWorld",data:()=>({drawer:!1,ecosystem:[{text:"vuetify-loader",href:"https://github.com/vuetifyjs/vuetify-loader"},{text:"github",href:"https://github.com/vuetifyjs/vuetify"},{text:"awesome-vuetify",href:"https://github.com/vuetifyjs/awesome-vuetify"}],importantLinks:[{text:"Documentation",href:"https://vuetifyjs.com"},{text:"Chat",href:"https://community.vuetifyjs.com"},{text:"Made with Vuetify",href:"https://madewithvuejs.com/vuetify"},{text:"Twitter",href:"https://twitter.com/vuetifyjs"},{text:"Articles",href:"https://medium.com/vuetify"}],whatsNext:[{text:"Explore components",href:"https://vuetifyjs.com/components/api-explorer"},{text:"Select a layout",href:"https://vuetifyjs.com/getting-started/pre-made-layouts"},{text:"Frequently Asked Questions",href:"https://vuetifyjs.com/getting-started/frequently-asked-questions"}]})},x=w,k=n(8320),Z=n(4542),j=n(26),V=n(6428),_=n(6816),O=n(7620),A=n(6651),T=n(459),E=n(3901),C=n(3970),N=n(7921),L=(0,s.Z)(x,b,y,!1,null,null,null),P=L.exports;l()(L,{VAppBar:k.Z,VAppBarNavIcon:Z.Z,VCard:j.Z,VIcon:V.Z,VList:_.Z,VListItem:O.Z,VListItemGroup:A.Z,VListItemIcon:T.Z,VListItemTitle:E.V9,VNavigationDrawer:C.Z,VToolbarTitle:N.qW});var S={name:"HomeView",components:{HelloWorld:P}},I=S,q=(0,s.Z)(I,h,g,!1,null,null,null),F=q.exports;r.Z.use(m.Z);const M=[{path:"/",name:"home",component:F},{path:"/about",name:"about",component:()=>n.e(443).then(n.bind(n,1872))}],B=new m.Z({mode:"history",base:"/static/",routes:M});var H=B,$=n(629);r.Z.use($.ZP);var W=new $.ZP.Store({state:{},getters:{},mutations:{},actions:{},modules:{}}),D=n(1910);r.Z.use(D.Z);var z=new D.Z({theme:{themes:{light:{primary:"#00bcd4",accent:"#ff9800"}}}});r.Z.config.productionTip=!1,new r.Z({router:H,store:W,vuetify:z,render:e=>e(v)}).$mount("#app")}},t={};function n(r){var o=t[r];if(void 0!==o)return o.exports;var i=t[r]={exports:{}};return e[r](i,i.exports,n),i.exports}n.m=e,function(){var e=[];n.O=function(t,r,o,i){if(!r){var a=1/0;for(l=0;l<e.length;l++){r=e[l][0],o=e[l][1],i=e[l][2];for(var u=!0,s=0;s<r.length;s++)(!1&i||a>=i)&&Object.keys(n.O).every((function(e){return n.O[e](r[s])}))?r.splice(s--,1):(u=!1,i<a&&(a=i));if(u){e.splice(l--,1);var c=o();void 0!==c&&(t=c)}}return t}i=i||0;for(var l=e.length;l>0&&e[l-1][2]>i;l--)e[l]=e[l-1];e[l]=[r,o,i]}}(),function(){n.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return n.d(t,{a:t}),t}}(),function(){n.d=function(e,t){for(var r in t)n.o(t,r)&&!n.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})}}(),function(){n.f={},n.e=function(e){return Promise.all(Object.keys(n.f).reduce((function(t,r){return n.f[r](e,t),t}),[]))}}(),function(){n.u=function(e){return"js/about.6ae00a5a.js"}}(),function(){n.miniCssF=function(e){}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={},t="frontend:";n.l=function(r,o,i,a){if(e[r])e[r].push(o);else{var u,s;if(void 0!==i)for(var c=document.getElementsByTagName("script"),l=0;l<c.length;l++){var f=c[l];if(f.getAttribute("src")==r||f.getAttribute("data-webpack")==t+i){u=f;break}}u||(s=!0,u=document.createElement("script"),u.charset="utf-8",u.timeout=120,n.nc&&u.setAttribute("nonce",n.nc),u.setAttribute("data-webpack",t+i),u.src=r),e[r]=[o];var d=function(t,n){u.onerror=u.onload=null,clearTimeout(v);var o=e[r];if(delete e[r],u.parentNode&&u.parentNode.removeChild(u),o&&o.forEach((function(e){return e(n)})),t)return t(n)},v=setTimeout(d.bind(null,void 0,{type:"timeout",target:u}),12e4);u.onerror=d.bind(null,u.onerror),u.onload=d.bind(null,u.onload),s&&document.head.appendChild(u)}}}(),function(){n.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){n.p="/static/"}(),function(){var e={143:0};n.f.j=function(t,r){var o=n.o(e,t)?e[t]:void 0;if(0!==o)if(o)r.push(o[2]);else{var i=new Promise((function(n,r){o=e[t]=[n,r]}));r.push(o[2]=i);var a=n.p+n.u(t),u=new Error,s=function(r){if(n.o(e,t)&&(o=e[t],0!==o&&(e[t]=void 0),o)){var i=r&&("load"===r.type?"missing":r.type),a=r&&r.target&&r.target.src;u.message="Loading chunk "+t+" failed.\n("+i+": "+a+")",u.name="ChunkLoadError",u.type=i,u.request=a,o[1](u)}};n.l(a,s,"chunk-"+t,t)}},n.O.j=function(t){return 0===e[t]};var t=function(t,r){var o,i,a=r[0],u=r[1],s=r[2],c=0;if(a.some((function(t){return 0!==e[t]}))){for(o in u)n.o(u,o)&&(n.m[o]=u[o]);if(s)var l=s(n)}for(t&&t(r);c<a.length;c++)i=a[c],n.o(e,i)&&e[i]&&e[i][0](),e[i]=0;return n.O(l)},r=self["webpackChunkfrontend"]=self["webpackChunkfrontend"]||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))}();var r=n.O(void 0,[998],(function(){return n(3783)}));r=n.O(r)})();
//# sourceMappingURL=app.9f15a627.js.map