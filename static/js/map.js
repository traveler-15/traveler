'use strict';

// 저장되어 있는 여행지 보여주기
$(document).ready(function () {
   show_place();
});
const show_place = function () {
   fetch('/place/show').then(res => res.json()).then(data => {
      let rows = data['result']
      $('#show_list').empty
      rows.forEach((v) => {
         let title = v['title'].replace('<b>', '').replace('</b>', ''), // 이름
            link = v['link'], // 링크
            address = v['address'], // 주소
            mapx = v['mapx'], // x좌표
            mapy = v['mapy']; // y좌표
         let temp_html = `<div class="card">
                              <div class="card-body">
                                 <blockquote class="blockquote mb-0">
                                    <p>이름 : ${title} </p>
                                    <a href = '#'><p id = "find_search" onclick="select_map(${mapx}, ${mapy})">위치 : ${address}</p></a>
                                    <a href = "${link}"><p>${link}</p></a>
                                                                     </blockquote>
                              </div>
                           </div>`
         $('#show_list').append(temp_html);

      })
   })
}

// 가고싶은 여행지 검색 및 리스트 띄우기
const search_place = function () {
   let query = $("#name").val();
   let formData = new FormData();
   formData.append("query_give", query);

   fetch("/place/search", { method: "POST", body: formData })
      .then((res) => res.json())
      .then((data) => {
         let rows = data // 배열 안에 객체

         // 0번째 위치값 선정 후 좌표 전달
         let first_place = new naver.maps.LatLng(rows[0]['mapx'], rows[0]['mapy'])
         map.setCenter(first_place);

         // 리스트 비워두기
         $('#search_list').empty();
         // rows 반복문 진행 -> 5개의 여행지 리스트 출력
         rows.forEach((v) => {
            let title = v['title'].replace('<b>', '').replace('</b>', ''), // 이름
               link = v['link'], // 링크
               address = v['address'], // 주소
               mapx = v['mapx'], // x좌표
               mapy = v['mapy']; // y좌표
            // temp_html 템플릿 출력하기
            let temp_html = `<div class="card">
                              <div class="card-body">
                                 <blockquote class="blockquote mb-0">
                                    <p>이름 : ${title} </p>
                                    <a href = '#'><p id = "find_search" onclick="select_map(${mapx}, ${mapy})">위치 : ${address}</p></a>
                                    <a href = "${link}"><p>${link}</p></a>
                                    <button id ="save" onclick="save_map('${title}', '${link}', '${address}', '${mapx}', '${mapy}')" type="button" class="btn btn-dark">찜</button>
                                 </blockquote>
                              </div>
                           </div>`
            $('#search_list').append(temp_html);
         })
      });
}


const save_map = function (title, link, address, mapx, mapy) {
   // formdata 만들기
   // save_map에서 데이터 받아오기
   let formData = new FormData();
   formData.append("title_give", title);
   formData.append("link_give", link);
   formData.append("address_give", address);
   formData.append("mapx_give", mapx);
   formData.append("mapy_give", mapy);

   // fetch로 app.py에 데이터 보내기.
   fetch('/place/save', { method: "POST", body: formData })
      .then((response) => response.json())
      .then((data) => {
         alert(data["msg"]);
      });

};


// 초기 Map 설정
let xMap = 37.3595704
let yMap = 127.105399


// Map Option 기능
let mapOptions = {
   center: new naver.maps.LatLng(xMap, yMap),
   zoomControl: true,
   zoomControlOptions: {
      style: naver.maps.ZoomControlStyle.SMALL,
      position: naver.maps.Position.TOP_RIGHT
   },
   zoom: 16
};

// Map을 templates에 띄우는 코드
let map = new naver.maps.Map(document.querySelector("#map"), mapOptions);

// let marker = new naver.maps.Marker({
//    position: new naver.maps.LatLng(xMap, yMap),
//    map: map
// });

