(function(){
  function toggle(btn){
    var id=btn.getAttribute('data-mo'), box=document.getElementById(id), open=btn.getAttribute('aria-expanded')==='true';
    if(box){ box.hidden=open; }
    document.querySelectorAll('.an-o[data-o="'+id+'"]').forEach(function(s){ s.style.visibility=open?'hidden':'visible'; });
    btn.setAttribute('aria-expanded', open?'false':'true');
    btn.textContent = open ? btn.dataset.label : btn.dataset.label.replace(/^Mở:?\s*/, 'Ẩn ');
    // mở đáp án của câu biểu quyết thì tô phương án đúng trong cùng màn
    var sec=btn.closest('.man');
    if(sec && (/^(a|r)/.test(id) || btn.hasAttribute('data-to'))){ sec.querySelectorAll('ol.opt li[data-dung]').forEach(function(li){ li.classList.toggle('dung', !open); }); }
  }
  document.querySelectorAll('[data-chep]').forEach(function(d){ var s=document.querySelector('#'+d.dataset.chep+' .fig svg'); if(s) d.appendChild(s.cloneNode(true)); });
  document.querySelectorAll('button.mo').forEach(function(b){
    b.dataset.label=b.textContent; b.setAttribute('aria-expanded','false');
    var id=b.getAttribute('data-mo'); if(document.getElementById(id)) b.setAttribute('aria-controls',id);
    b.addEventListener('click',function(){toggle(b)});
  });
  document.querySelectorAll('.an-o').forEach(function(s){ s.style.visibility='hidden'; });
  var mans=[].slice.call(document.querySelectorAll('.man'));
  function cur(){ var y=window.scrollY+window.innerHeight*0.35, k=0; mans.forEach(function(s,i){ if(s.offsetTop<=y) k=i; }); return k; }
  function go(d){ var k=Math.max(0,Math.min(mans.length-1,cur()+d)); mans[k].scrollIntoView({behavior:'smooth'}); }
  // clip có điểm dừng: bắt đầu từ data-bat, tự dừng ở mỗi .buoc[data-dung] và ở data-het; Enter/Space/bấm video = phát tiếp
  var vgs=[].slice.call(document.querySelectorAll('.vg')).map(function(g){
    var v=g.querySelector('video'), sec=g.closest('.man'), bs=[].slice.call(g.querySelectorAll('.buoc'));
    var bat=+g.dataset.bat, het=+g.dataset.het, raf=0, chay=false, o=-1;
    var dung=bs.filter(function(b){return b.hasAttribute('data-dung')}).map(function(b){return +b.dataset.t}).concat([het]);
    var qua=dung.map(function(){return false});
    var moc=sec.querySelector('.moc'), nutTiep=sec.querySelector('[data-v="tiep"]');
    dung.forEach(function(){ moc.appendChild(document.createElement('i')); });
    function ve(){
      var t=chay?v.currentTime:-1, hien=bs[0];
      if(o>=0) t=dung[o];   // đang đứng ở điểm dừng: hiện đúng ô của điểm đó
      bs.forEach(function(b){ if(+b.dataset.t<=t+0.001) hien=b; });
      bs.forEach(function(b){ b.classList.toggle('hien', b===hien); });
      [].forEach.call(moc.children,function(c,i){ c.classList.toggle('qua', qua[i]); });
      nutTiep.textContent = qua[qua.length-1] ? '→ Sang màn sau' : (!chay ? '▶ Phát' : (v.paused ? '▶ Phát tiếp' : '❚❚ Tạm dừng'));
    }
    function lap(){
      var t=v.currentTime;
      for(var i=0;i<dung.length;i++){ if(!qua[i] && t>=dung[i]-0.02){ qua[i]=true; o=i; v.pause(); break; } }
      ve(); if(!v.paused) raf=requestAnimationFrame(lap);
    }
    v.addEventListener('play',function(){ o=-1; cancelAnimationFrame(raf); raf=requestAnimationFrame(lap); ve(); });
    v.addEventListener('pause',ve);
    function tiep(){
      if(qua[qua.length-1]){ go(1); return; }
      if(!chay){ chay=true; v.currentTime=bat; }
      if(v.paused) v.play(); else v.pause();
    }
    function lai(){
      if(!chay) return;
      var t=v.currentTime, tu=bat;
      dung.forEach(function(d,i){ if(qua[i] && d<t-0.3) tu=d; });
      dung.forEach(function(d,i){ if(d>tu+0.001) qua[i]=false; });
      o=-1; v.currentTime=tu; v.play();
    }
    v.addEventListener('click',tiep);
    nutTiep.addEventListener('click',tiep);
    sec.querySelector('[data-v="lai"]').addEventListener('click',lai);
    ve();
    return {sec:sec, tiep:tiep};
  });
  document.addEventListener('keydown',function(e){
    var t=e.target;
    if(t.isContentEditable){ if(e.key==='Enter'||e.key==='Escape'){ e.preventDefault(); t.blur(); } return; }
    if(t.closest && (t.closest('button')||t.closest('video')) && (e.key==='Enter'||e.key===' ')) return;
    var vg=vgs.filter(function(x){return x.sec===mans[cur()]})[0];
    if(vg && (e.key==='Enter'||e.key===' ')){ e.preventDefault(); vg.tiep(); return; }
    if(e.key==='ArrowRight'||e.key==='PageDown'){ e.preventDefault(); go(1); }
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){ e.preventDefault(); go(-1); }
    else if(e.key==='Enter'){ var b=mans[cur()].querySelector('button.mo[aria-expanded="false"]'); if(b){ e.preventDefault(); toggle(b); } }
  });
  // rời màn thì dừng clip đang chạy
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){ es.forEach(function(en){ if(!en.isIntersecting) en.target.pause(); }); },{threshold:.2});
    document.querySelectorAll('video').forEach(function(v){ io.observe(v); });
  }
  document.addEventListener('DOMContentLoaded',function(){
    if(window.renderMathInElement) renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false});
  });
})();
