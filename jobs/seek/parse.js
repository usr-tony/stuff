const raw = process.argv[2]
const data = eval(raw)
process.stdout.write(JSON.stringify(data))