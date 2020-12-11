

var tableInfo = document.getElementById("tableInfo");  // 获取table中的内容

    var totalRow = tableInfo.rows.length;  // 获取table行数
    window.alert(totalRow);
    //var cells = departmentsInfo.rows[0].cells.length;  // 获取列数
    var pagesize = 2;   // 每页两条
    var totalPage = Math.ceil(totalRow/pagesize);  // 计算出总页数=总条数/每页条数
    var currentPage;   // 当前页
    var startRow;
    var lastRow;

    // 定义一个换页的函数
    function pagination(i){
      currentPage = i;
      startRow = (currentPage-1)*pagesize;  //每页显示第一条数据的行数
      lastRow = currentPage*pagesize;  // 每页显示的最后一条数据的行数
      document.getElementById("numPage").innerHTML="第"+currentPage+"页";

      if(lastRow>totalRow){
           lastRow=totalRow;// 如果最后一页的最后一条数据显示的行数大于总条数，就让最后一条的行数等于总条数
      }
      //将数据遍历出来
      for(var i=0; i<totalRow; i++){
        var hrow = tableInfo.rows[i];
        if( i>=startRow && i<lastRow ){
          hrow.style.color="#000";
          hrow.style.display="table-row";   // 将循环出来的每一行信息作为一个tr显示到页面
        }else{
          hrow.style.display="none";
        }
      }
    }

    $(function(){ firstPage(); });

    function firstPage(){
      var i = 1;
      pagination(i);
    }
    function prevPage(){
      var i= currentPage-1;
      if(i<1) i=currentPage;
      pagination(i);
    }
    function pnextPage(){
      var i= currentPage+1;
      if(i>totalPage) i= currentPage;
      pagination(i);
    }
    function lastPage(){
      var i = totalPage;
      pagination(i);
    }