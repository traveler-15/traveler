'use strict';

// 저장되어 있는 여행지 보여주기
const show_place = function() {

}

// 가고싶은 여행지 검색 및 리스트 띄우기
const search_place = function () {
   let query = $("#name").val();
   let formData = new FormData();
   formData.append("query_give", query);

   fetch ("/place/search", { method: "POST", body: formData })
      .then((res) => res.json())
      .then((data) => {
         let rows = data
         // 0번째 위치값 선정 후 좌표 전달
         let first_place = new naver.maps.LatLng(rows[0]['mapx'], rows[0]['mapy'])
         map.setCenter(first_place);

         // find_search_${count} 숫자 다르게 하기
         let count = 0
         // 리스트 비워두기
         $('#search_list').empty();
         // rows 반복문 진행 -> 5개의 여행지 리스트 출력
         rows.forEach((v) => {
            let title = v['title'], // 이름
            link = v['link'], // 링크
            address = v['address'], // 주소
            xMap = v['mapx'], // x좌표
            yMap = v['mapy']; // y좌표
            // temp_html 템플릿 출력하기
            let temp_html =`<div class="card">
                              <div class="card-body">
                                 <blockquote class="blockquote mb-0">
                                    <p>이름 : ${title} </p>
                                    <a href = '#'><p id = "find_search_${count}" onclick='select_map(${count},${xMap},${yMap})'>위치 : ${address}</p></a>
                                    <a href = "${link}"><p>${link}</p></a>
                                 </blockquote>
                              </div>
                           </div>`
            $('#search_list').append(temp_html);
            count =+ 1
         })
   });
}


// 여행지 저장하기
const save_map = function() {

}
// 여행지 찾기, 버튼 클릭했을 경우 해당 위치로 이동
const select_map = function(count,xMap,yMap) {
   var find_map = new naver.maps.LatLng(xMap, yMap)
   $(`#find_search_${count}`).on("click", function(e) {
      console.log(xMap,yMap)
      e.preventDefault();
      map.setCenter(find_map);
   });
}


// 초기 Map 설정
// let xMap = 37.3595704
// let yMap = 127.105399


// Map Option 기능
let mapOptions = {
   center: new naver.maps.LatLng(37.3595704, 127.105399),
   zoomControl: true,
   zoomControlOptions: {
      style: naver.maps.ZoomControlStyle.SMALL,
      position: naver.maps.Position.TOP_RIGHT
   },
   zoom: 10
};

// Map을 templates에 띄우는 코드
let map = new naver.maps.Map(document.querySelector("#map"), mapOptions);


// 버튼 입력하기 예제
// $("#to-jeju").on("click", function(e) {
//    e.preventDefault();

//    map.setCenter(jeju);
// });

// let marker = new naver.maps.Marker({
//    position: new naver.maps.LatLng(xMap, yMap),
//    map: map
// });

