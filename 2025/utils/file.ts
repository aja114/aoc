import fs from "fs";
import path from "path";
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function readInput(inputFile: string): string{
    const filePath = path.join(__dirname, "../inputs", inputFile);
    const data = fs.readFileSync(filePath).toString()
    return data
}
