const fs = require('fs');
const path = require('path');
const child_process = require('child_process');
const exec = child_process.exec;
require('dotenv').config({path: "/home/runner/Tools/coderunner/.env"})


const TMP_ROOT = process.env.TMP_ROOT;



class ProcessResult {
  constructor() {
    this.error = null;
    this.stderr = '';
    this.stdout = '';
    this.func_return = null;
  }
  print() {
    console.log("====== ProcessResult ======");
    console.log("error:", this.error);
    console.log("stdout:", this.stdout);
    console.log("stderr:", this.stderr);
    console.log("func_return:", this.func_return);
    console.log("===========================\n");
  }
}



function run_js_codestr(codestr) {
  return new Promise((resolve) => {
    const tmpPath = path.join(TMP_ROOT, `code_${Date.now()}.js`);

    fs.writeFileSync(tmpPath, codestr);

    let process_result = new ProcessResult();

    exec(`node ${tmpPath}`, (error, stdout, stderr) => {
      fs.unlinkSync(tmpPath); // Delete the temporary file

      process_result.error = error;
      process_result.stderr = stderr;
      process_result.stdout = stdout;
      resolve(process_result); 
    });
  });
}



function run_js_funcstr(funcstr, func_name, func_args) {
  return new Promise((resolve) => {
    const TMP_ROOT = process.env.TMP_ROOT || os.tmpdir();
    const tmpPath = path.join(TMP_ROOT, `code_${Date.now()}.js`);
    const process_result = new ProcessResult();

    const wrappedCode = `${funcstr}\n\nmodule.exports = { ${func_name} };`;
    fs.writeFileSync(tmpPath, wrappedCode);

    const mod = require(tmpPath);
    const func = mod[func_name];

    if (typeof func !== 'function') {
      throw new Error(`Not found: '${func_name}'`);
    }

    const stdoutBuffer = [];
    const originalLog = console.log;
    try {
      // Capture console.log output
      console.log = (...args) => {
        stdoutBuffer.push(args.join(' '));
      };
    
      // Run function
      const result = func(func_args);
      process_result.func_return = result;
    
      // Back to original console.log
      console.log = originalLog;
    
      process_result.stdout = stdoutBuffer.join('\n');
    } catch (error) {
      console.log = originalLog;  
      process_result.error = error;
      process_result.stderr = error.message;
      resolve(process_result);
    }
    
    // Delete the temporary file
    delete require.cache[require.resolve(tmpPath)];
    fs.unlinkSync(tmpPath);
    resolve(process_result);


  });
}




const funcstr = `
function square({ x }) {
  console.log("hello world");
  return x * x;
  // return "hello world";
}
`;




(async () => {
  const process_result = await run_js_funcstr(funcstr, 'square', { x: 9 });
  process_result.print();
})();
