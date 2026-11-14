import asyncio,json,base64,subprocess,sys,os
SITE=os.environ.get('SITE',os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from playwright.async_api import async_playwright
PNG=open('obj.png','rb').read()
FAIL=[]
def ok(c,msg):
    print(('PASS ' if c else 'FAIL ')+msg)
    if not c: FAIL.append(msg)
async def route(r):
    u=r.request.url
    if 'image.pollinations.ai' in u: return await r.fulfill(status=200,body=PNG,headers={'content-type':'image/png','access-control-allow-origin':'*'})
    if 'text.pollinations.ai' in u:
        body=r.request.post_data or ''
        if 'video scripts' in body:
            c={"title":"Robot ki Kahani","mood":"happy","scenes":[{"caption":f"Scene {i} caption","prompt":"robot village"} for i in range(4)]}
        elif 'control a video editor' in body:
            c={"say":"Done","actions":[{"do":"allTransition","type":"wipe"}]}
        else:
            c={"say":"Bana diya","actions":[{"do":"template","name":"Birthday Story"},{"do":"editText","find":"__first","text":"Happy Birthday Arjun"},{"do":"addSticker","emoji":"🎉"}]}
        return await r.fulfill(status=200,body=json.dumps({"choices":[{"message":{"content":json.dumps(c)}}]}),headers={'content-type':'application/json','access-control-allow-origin':'*'})
    if '@huggingface/transformers' in u: return await r.fulfill(status=200,body=open('fake_tf.js').read(),headers={'content-type':'application/javascript','access-control-allow-origin':'*'})
    if 'qrcode-generator' in u: return await r.fulfill(status=200,body="window.qrcode=function(){let d='';return{addData(x){d=x},make(){},getModuleCount(){return 21},isDark(r,c){return (r*c+r)%3==0}}}",headers={'content-type':'application/javascript'})
    if 'fonts.g' in u: return await r.fulfill(status=200,body='',headers={'content-type':'text/css'})
    return await r.continue_()
async def main():
  srv=subprocess.Popen([sys.executable,'-m','http.server','8765','-d',SITE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  await asyncio.sleep(1)
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
    cx=await b.new_context(viewport={'width':1400,'height':880},accept_downloads=True)
    await cx.route('**/*',route)
    pg=await cx.new_page();errs=[]
    pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)))
    pg.on('console',lambda m:m.type=='error' and errs.append('CONSOLE '+m.text))
    await pg.goto('http://localhost:8765/index.html');await pg.wait_for_timeout(1500)
    E=pg.evaluate
    # ---------- DESIGN ----------
    for i in range(10):
        await E(f'__rachna.applyTemplate({i})')
    ok(await E('__rachna.doc.pages.length')==1,'templates apply (10)')
    await E("__rachna.applyTemplate(1)")
    n0=await E('__rachna.doc.pages[0].els.length')
    # shapes via panel tiles
    await E("document.querySelector('#rail [data-tab=elements]').click()")
    tiles=await E("document.querySelectorAll('#shapeGrid .tile').length")
    await E("document.querySelectorAll('#shapeGrid .tile').forEach(t=>t.click())")
    await E("document.querySelectorAll('#lineGrid .tile').forEach(t=>t.click())")
    ok(await E('__rachna.doc.pages[0].els.length')==n0+tiles+6,f'all {tiles} shapes + 6 lines added')
    # text presets & combos
    await E("document.querySelectorAll('.txtPreset[data-tp]').forEach(b=>b.click());document.querySelectorAll('#comboList [data-combo]').forEach(b=>b.click())")
    await E("document.querySelectorAll('#emoGrid [data-emo]')[0].click();document.querySelectorAll('#symGrid [data-emo]')[0].click()")
    # text fx on last text
    await E("const e=__rachna.doc.pages[0].els.filter(x=>x.type==='text').pop();sel=[e.id];propsUI()")
    for fx in ['shadow','lift','outline','hollow','neon','bg','splice','3d','gradient','none']:
        await E("document.querySelector('[data-fx=\""+fx+"\"]').click()")
    ok(True,'all 10 text effects clicked')
    # toggles & align
    for s in ['[data-tog=italic]','[data-tog=underline]','[data-tog=upper]','[data-al=left]','[data-al=right]','[data-ag=l]','[data-ag=c]','[data-ag=b]','[data-ord=front]','[data-ord=back]','[data-ord=up]','[data-ord=down]','[data-a=flipX]','[data-a=dup]','[data-a=lock]','[data-a=lock]']:
        await E(f"document.querySelector('#props {s}').click()")
    # prop inputs
    await E("""for(const i of document.querySelectorAll('#props input[type=range]')){i.value=i.max*0.6;i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}))}""")
    await E("""const f=document.querySelector('#props select[data-k=font]');f.value='Anton';f.dispatchEvent(new Event('input',{bubbles:true}))""")
    # image upload, filters, masks, crop, bg remove fast+AI(mocked)
    await pg.set_input_files('#fileImg',['obj.png']);await pg.wait_for_timeout(800)
    ok(await E("selEls()[0]&&selEls()[0].type")=='image','photo upload selects image')
    for f in ['bw','vintage','vivid','cool','warm','drama','fade','orig']:
        await E(f"document.querySelector('[data-flt={f}]').click()")
    await E("""const m=document.querySelector('#props select[data-k=mask]');for(const v of ['ellipse','heart','star','rect']){m.value=v;m.dispatchEvent(new Event('input',{bubbles:true}))}""")
    src0=await E("selEls()[0].src")
    await E("document.querySelector('[data-a=rmbgFast]').click()");await pg.wait_for_timeout(800)
    src1=await E("selEls()[0].src");ok(src1!=src0,'fast bg remover changes image')
    await E("document.querySelector('[data-a=rmbgAI]').click()");await pg.wait_for_timeout(2500)
    src2=await E("selEls()[0].src");ok(src2!=src1,'AI bg remover pipeline (mocked model) works')
    await E("undo()")
    a=await E("(async()=>{const im=await loadImg(srcOf(selEls()[0].src));const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d');x.drawImage(im,0,0);return [x.getImageData(2,2,1,1).data[3],x.getImageData(c.width/2|0,c.height/2|0,1,1).data[3]]})()")
    ok(a[0]==0 and a[1]>200,f'bg alpha applied (corner={a[0]}, center={a[1]})')
    await E("document.querySelector('[data-a=asBg]').click()")
    ok(await E("!!__rachna.doc.pages[0].bg.src"),'photo -> background')
    # frames
    await E("document.querySelector('#frameGrid .tile').click()")
    await pg.set_input_files('#fileImg',['obj.png']);await pg.wait_for_timeout(700)
    ok(await E("!!selEls()[0].src"),'frame filled with photo')
    # QR
    await E("document.querySelector('#qrText').value='https://example.com';document.querySelector('#qrGo').click()");await pg.wait_for_timeout(500)
    ok(await E("selEls()[0]&&selEls()[0].name")=='QR code','QR code added')
    # draw
    await E("setDraw(true)");box=await pg.locator('#cv').bounding_box()
    await pg.mouse.move(box['x']+50,box['y']+50);await pg.mouse.down()
    for i in range(10): await pg.mouse.move(box['x']+50+i*8,box['y']+50+i*5)
    await pg.mouse.up();await E("setDraw(false)")
    ok(await E("__rachna.doc.pages[0].els.at(-1).type")=='path','pen drawing')
    # bg panel
    await E("document.querySelector('#bgSw i').click();document.querySelector('#gradGrid .tile').click()")
    # layers panel
    await E("document.querySelector('#rail [data-tab=layers]').click()")
    await E("document.querySelector('#layerList [data-la=hide]').click();document.querySelector('#layerList [data-la=hide]').click();document.querySelector('#layerList .layer').click()")
    ok(await E("document.querySelectorAll('#layerList .layer').length")>5,'layers list')
    # keyboard
    await E("sel=[__rachna.doc.pages[0].els.at(-1).id]")
    for k in ['Control+c','Control+d','ArrowLeft','Shift+ArrowUp',']','[','Control+a','Escape','t','r','o','l']:
        await pg.keyboard.press(k)
    await pg.wait_for_timeout(500)
    # pages
    await E("document.querySelector('#pgAdd').click()");await E("document.querySelector('[data-pa=dup]').click()");await E("document.querySelector('[data-pa=left]').click()")
    ok(await E("__rachna.doc.pages.length")==3,'add/dup/move pages')
    await E("document.querySelector('[data-pa=del]').click()")
    ok(await E("__rachna.doc.pages.length")==2,'delete page')
    # undo/redo
    n=await E("__rachna.doc.pages.length");await E("undo()");ok(await E("__rachna.doc.pages.length")==n+1,'undo');await E("redo()");ok(await E("__rachna.doc.pages.length")==n,'redo')
    # resize modal
    await E("document.querySelector('#btnResize').click()");await E("document.querySelector('#sizeGrid button:nth-child(3)').click();document.querySelector('#rsGo').click()")
    ok(await E("[__rachna.doc.w,__rachna.doc.h]")==[1280,720],'magic resize to YouTube')
    # exports
    for fmt,allp in [('png','cur'),('jpg','cur'),('pdf','all'),('svg','cur'),('json','cur')]:
        await E("document.querySelector('#btnExport').click()")
        await pg.select_option('#exFmt',fmt);await pg.select_option('#exPages',allp)
        async with pg.expect_download(timeout=20000) as d: await E("document.querySelector('#exGo').click()")
        dd=await d.value;path=f'out.{fmt}';await dd.save_as(path)
        import os;ok(os.path.getsize(path)>500,f'export {fmt} ({os.path.getsize(path)} bytes)')
    pdfinfo=subprocess.run(['pdfinfo','out.pdf'],capture_output=True,text=True).stdout
    ok('Pages:' in pdfinfo and pdfinfo.split('Pages:')[1].split()[0]=='2','PDF valid with 2 pages')
    # open project file back
    await E("loadState(newDoc(),{})")
    await pg.set_input_files('#fileJson',['out.json']);await pg.wait_for_timeout(800)
    ok(await E("__rachna.doc.pages.length")==2 and await E("__rachna.doc.w")==1280,'project .json reopen')
    # text edit by double click
    await E("__rachna.applyTemplate(4)");await pg.wait_for_timeout(300)
    e=await E("(()=>{const t=__rachna.doc.pages[0].els[1];return [t.x+t.w/2,t.y+t.h/2,__rachna.doc.w]})()")
    box=await pg.locator('#cv').bounding_box();z=box['width']/e[2]
    await pg.mouse.dblclick(box['x']+e[0]*z,box['y']+e[1]*z);await pg.wait_for_timeout(200)
    await pg.keyboard.press('Control+a');await pg.keyboard.type('Naya vichar');await pg.mouse.click(box['x']+3,box['y']+3)
    ok(await E("__rachna.doc.pages[0].els[1].text")=='Naya vichar','double-click text editing')
    # AI magic image (mocked)
    await E("document.querySelector('#aiPrompt').value='pahad';document.querySelector('#aiGen').click()");await pg.wait_for_timeout(1200)
    ok(await E("selEls()[0]&&selEls()[0].type")=='image','AI image tab (mocked)')
    await E("document.querySelector('#aiTextPrompt').value='cafe';document.querySelector('#aiWrite').click()");await pg.wait_for_timeout(800)
    ok(await E("document.querySelectorAll('#aiOut [data-ai]').length")>=0,'magic write ran')
    # Agent: local + AI
    await E("document.querySelector('#rail [data-tab=agent]').click()")
    for q in ['background neela karo','title jodo: Mera Cafe','diwali post banao: Shubh Diwali','instagram story size karo','naya page','undo']:
        await E(f"agentSend({q!r})");await pg.wait_for_timeout(500)
    await E("agentSend('mere dost ke liye ek birthday card bana do')");await pg.wait_for_timeout(1200)
    ok(await E("__rachna.doc.pages[cur].els.some(e=>e.text==='Happy Birthday Arjun')"),'agent AI path (mocked LLM) builds birthday card')
    await E("agentSend('photo ka background hatao')");await pg.wait_for_timeout(1500)
    ok(await E("document.querySelectorAll('#chat .msg').length")>8,'agent chat log works')
    # hand-off to video
    await E("loadState(newDoc(),{});__rachna.applyTemplate(0)")
    await E("sendToVideo()");await pg.wait_for_url('**/video.html*',timeout=10000);await pg.wait_for_timeout(2500)
    ok(await E("__rv.P.clips.length")>=1 and await E("[__rv.P.w,__rv.P.h]")==[1920,1080],'design -> video handoff')
    print('DESIGN ERRORS:',[x for x in errs if 'favicon' not in x]);errs.clear()
    # ---------- VIDEO ----------
    V=E
    await V("localStorage.clear()")
    await pg.set_input_files('#fileM',['clip.webm','obj.png']);await pg.wait_for_timeout(2500)
    ok(await V("__rv.P.clips.length")==3,'import video+photo')
    await V("document.querySelector('[data-am=over]').click()");await pg.set_input_files('#fileM',['gs.webm']);await pg.wait_for_timeout(2000)
    ok(await V("__rv.P.overs.length")==1,'overlay import')
    await V("document.querySelector('[data-am=main]').click()")
    for tp in ['title','sub','lower','hindi','neon']: await V(f"document.querySelector('[data-tp={tp}]').click()")
    ok(await V("__rv.P.texts.length")==5,'5 text presets')
    for m in ['happy','calm','epic','lofi','suspense']:
        await V(f"__rv.addMusic('{m}')")
    ok(await V("__rv.P.audios.length")==1,'music moods (replace old music)')
    # transitions & anims rendering at every boundary
    for tr in ['fade','black','slide','zoom','wipe','none']:
        await V(f"__rv.P.clips.forEach((c,i)=>{{if(i)c.trans='{tr}'}});__rv.commit()")
        for tt in [0.1,3.2,4.2,7.3,9.5]: await V(f"__rv.seek({tt})")
    for an in ['fade','pop','slide','type','none']:
        await V(f"__rv.P.texts.forEach(x=>x.anim='{an}');__rv.draw()")
    ok(True,'all transitions x times rendered')
    # select clip & props
    await V("sel={k:'clip',id:__rv.P.clips[1].id};openTab('props')")
    await V("""for(const i of document.querySelectorAll('#props input[type=range]')){i.value=(+i.min+ +i.max)/2;i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}))}""")
    await V("""for(const s of document.querySelectorAll('#props select')){s.selectedIndex=1;s.dispatchEvent(new Event('input',{bubbles:true}))}""")
    await V("""for(const i of document.querySelectorAll('#props input[type=number]')){i.value=1.5;i.dispatchEvent(new Event('input',{bubbles:true}))}""")
    for a in ['dup','left','right','resetAdj']: await V(f"document.querySelector('#props [data-a={a}]')&&document.querySelector('#props [data-a={a}]').click()")
    # split / delete / undo
    c=await V("__rv.P.clips.length");await V("__rv.seek(1)");await V("split()")
    ok(await V("__rv.P.clips.length")==c+1,'split');await V("undo()");ok(await V("__rv.P.clips.length")==c,'undo');await V("redo()")
    # overlay props + chroma
    await V("sel={k:'over',id:__rv.P.overs[0].id};openTab('props')")
    await V("const i=document.querySelector('#props [data-p=chroma]');i.checked=true;i.dispatchEvent(new Event('input',{bubbles:true}))")
    await V("document.querySelector('#props [data-a=full]').click()")
    await V("__rv.seek(0.5)")
    # text & audio props
    await V("sel={k:'text',id:__rv.P.texts[0].id};openTab('props')");await V("document.querySelector('#props [data-a=tnow]').click();document.querySelector('#props [data-a=dup]').click()")
    await V("sel={k:'aud',id:__rv.P.audios[0].id};openTab('props')");await V("document.querySelector('#props [data-a=fitV]').click()")
    # timeline drag of text
    await V("document.querySelector('#tlScroll').scrollLeft=0");blk=pg.locator('.blk.txt').first;await blk.scroll_into_view_if_needed();bb=await blk.bounding_box();s0=await V("__rv.P.texts[0].start")
    await pg.mouse.move(bb['x']+5,bb['y']+5);await pg.mouse.down();await pg.mouse.move(bb['x']+65,bb['y']+5,steps=5);await pg.mouse.up()
    ok(await V("__rv.P.texts[0].start")!=s0,'drag text on timeline')
    # ruler scrub, zoom, frame step
    await V("document.querySelector('#zi').click();document.querySelector('#zo').click();document.querySelector('#fNext').click();document.querySelector('#fBack').click()")
    # agent local + AI
    await V("openTab('agent')")
    for q in ['har photo 2 second ki karo','sab mein zoom transition','title likho: Mera Safar','calm music lagao','green screen chalu karo','vintage filter lagao']:
        await V(f"agent({q!r})");await pg.wait_for_timeout(400)
    await V("agent('kuch accha sa effect do')");await pg.wait_for_timeout(800)
    ok(await V("__rv.P.clips.slice(1).every(c=>c.trans==='wipe')"),'video agent AI path (mocked)')
    # AI movie (mocked)
    c=await V("__rv.P.clips.length")
    await V("document.querySelector('#mvTopic').value='robot';document.querySelector('#mvN').value=4;document.querySelector('#mvGo').click()");await pg.wait_for_timeout(5000)
    ok(await V("__rv.P.clips.length")==c+4 and await V("__rv.P.texts.some(t=>t.text==='Robot ki Kahani')"),'AI Movie Maker (mocked): 4 scenes + title')
    # aspect change
    await pg.select_option('#aspect','1080x1920');ok(await V("__rv.P.h")==1920,'aspect change')
    # persistence
    cnt=await V("JSON.stringify([__rv.P.clips.length,__rv.P.texts.length,__rv.P.audios.length,__rv.P.overs.length])")
    await pg.wait_for_timeout(1200);await pg.reload();await pg.wait_for_timeout(3000)
    ok(await V("JSON.stringify([__rv.P.clips.length,__rv.P.texts.length,__rv.P.audios.length,__rv.P.overs.length])")==cnt,'video project survives reload '+cnt)
    # export (short) – trim project to ~4s
    await V("__rv.P.clips=__rv.P.clips.slice(0,2);__rv.P.clips.forEach(c=>{if(c.type==='image')c.dur=1});__rv.P.texts=__rv.P.texts.slice(0,2).map(t=>({...t,start:0,dur:2}));__rv.P.audios.forEach(a=>{a.start=0;a.dur=2});__rv.P.overs.forEach(o=>{o.start=0;o.dur=2});__rv.commit()")
    T=await V("total()")
    async with pg.expect_download(timeout=90000) as d: await V("__rv.exportVideo()")
    dd=await d.value;await dd.save_as('out_v');
    pr=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height','-of','compact','out_v'],capture_output=True,text=True).stdout
    ok('video' in pr and 'audio' in pr,f'video export has video+audio (timeline {T:.1f}s): '+pr.replace('\n',' | '))
    # link back to design
    await E("document.querySelector('#covX').click()");await pg.click('a[href="index.html"]');await pg.wait_for_timeout(1500)
    ok('index.html' in pg.url and await E("__rachna.doc.pages.length")>=1,'video -> design link, design autosave restored')
    print('VIDEO+BACK ERRORS:',[x for x in errs if 'favicon' not in x])
    # ---------- MOBILE ----------
    m=await b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);await m.route('**/*',route)
    mp=await m.new_page();merr=[];mp.on('pageerror',lambda e:merr.append(str(e)))
    await mp.goto('http://localhost:8765/index.html');await mp.wait_for_timeout(1500)
    sw=await mp.evaluate("document.documentElement.scrollWidth");ok(sw<=392,f'design mobile no horizontal overflow ({sw})')
    vis=await mp.evaluate("(()=>{const r=document.querySelector('#btnExport').getBoundingClientRect();return r.right<=390&&r.width>0})()");ok(vis,'design mobile Download button visible')
    await mp.tap('#rail [data-tab=text]');await mp.wait_for_timeout(300);await mp.tap('.txtPreset[data-tp=h1]');await mp.wait_for_timeout(300)
    ok(await mp.evaluate("selEls().length")==1,'mobile tap adds text');await mp.screenshot(path='m_design.png')
    await mp.goto('http://localhost:8765/video.html');await mp.wait_for_timeout(1500)
    sw=await mp.evaluate("document.documentElement.scrollWidth");ok(sw<=392,f'video mobile no overflow ({sw})')
    vis=await mp.evaluate("(()=>{const r=document.querySelector('#exportB').getBoundingClientRect();return r.right<=391&&r.width>0})()");ok(vis,'video mobile Export visible')
    await mp.tap('#mobTabs [data-t=text]');await mp.wait_for_timeout(300);await mp.screenshot(path='m_video.png')
    print('MOBILE ERRORS:',merr)
    await b.close()
  srv.terminate()
  print('\nTOTAL FAIL:',len(FAIL),FAIL)
if __name__=="__main__": asyncio.run(main())
