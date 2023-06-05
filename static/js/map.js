'use strict';

let xMap = 37.3595704
let yMap = 127.105399

// Map Option 기능
const mapOptions = {
   center: new naver.maps.LatLng(xMap, yMap),
   zoomControl: true,
   zoomControlOptions: {
      style: naver.maps.ZoomControlStyle.SMALL,
      position: naver.maps.Position.TOP_RIGHT
   },
   zoom: 15
};

let map = new naver.maps.Map(document.querySelector("#map"), mapOptions);

let marker = new naver.maps.Marker({
   position: new naver.maps.LatLng(xMap, yMap),
   map: map
});