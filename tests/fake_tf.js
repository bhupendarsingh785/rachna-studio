export const env={};
class T{constructor(w,h){this.w=w;this.h=h}sigmoid(){return this}mul(){return this}to(){return this}}
export class RawImage{constructor(d,w,h,c){this.data=d;this.width=w;this.height=h;this.channels=c}
 static async fromURL(u){const i=new Image();await new Promise(r=>{i.onload=r;i.src=u});return new RawImage(null,i.naturalWidth,i.naturalHeight,3)}
 static fromTensor(t){return {resize:async(w,h)=>{const d=new Uint8Array(w*h);for(let y=0;y<h;y++)for(let x=0;x<w;x++)d[y*w+x]=(Math.hypot(x-w/2,y-h/2)<Math.min(w,h)*.3)?255:0;return new RawImage(d,w,h,1)}}}}
export const AutoModel={from_pretrained:async(id,o)=>{if(o.progress_callback)o.progress_callback({status:'progress',file:'onnx/model_fp16.onnx',progress:50});return async()=>({output_image:[new T()]})}};
export const AutoProcessor={from_pretrained:async()=>async(img)=>({pixel_values:{}})};
