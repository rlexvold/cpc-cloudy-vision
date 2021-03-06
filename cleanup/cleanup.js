const commandLineArgs = require('command-line-args');
const fs = require('fs');
const path = require('path');

const optionDefinitions = [
    {name: 'directory', alias: 'd', type: String},
    {name: 'output', alias: 'o', type: String},
    {name: 'threshold', alias: 't', type: Number, defaultOption: 70}
];

const options = commandLineArgs(optionDefinitions);
const processors = new Map([
    ['clarifai', clarifai],
    ['google', google],
    ['ibm', ibm],
    ['imagga', imagga],
    ['msft', msft],
    ['rekognition', amazon]
]);

let images = new Map();

function ibm(input) {
    return input.images[0].classifiers[0].classes.filter(con => (con.score * 100) >= options.threshold).map((con) => {
        return {confidence: con.score * 100, tag: con.class};
    });
}

function google(input) {
    return input.responses[0].labelAnnotations.filter(con => (con.score * 100) >= options.threshold).map((con) => {
        return {confidence: con.score * 100, tag: con.description};
    });
}

function clarifai(input) {
    return input.outputs[0].data.concepts.filter(con => (con.value * 100) >= options.threshold).map((con) => {
        return {confidence: con.value * 100, tag: con.name};
    });
}

function imagga(input) {
    return input.results[0].tags.filter(con => con.confidence >= options.threshold).map((con) => {
        return {confidence: con.confidence, tag: con.tag};
    });
}

function msft(input) {
    return input.tags.filter(con => (con.confidence * 100) >= options.threshold).map((con) => {
        return {confidence: con.confidence * 100, tag: con.name};
    });
}

function amazon(input) {
    return input.Labels.filter(con => con.Confidence >= options.threshold).map((con) => {
        return {confidence: con.Confidence, tag: con.Name};
    });
}

function parseFileName(name) {
    const parts = name.split('.');
    return {image: parts[0], type: parts[2]};
}

if (!options.directory) {
    console.log('Provide a directory idiot');
    process.exit(1);
}

let files = fs.readdirSync(options.directory);
const jsonFiles = files.filter(f => f.includes('json'));

for (let file of jsonFiles) {
    const input = require(path.join(options.directory, file));
    const {image, type} = parseFileName(file);
    let theImage = images.get(image);
    if (!theImage) {
        theImage = {};
    }
    theImage[type] = processors.get(type)(input);
    images.set(image, theImage);
}

let fileOut = fs.createWriteStream(options.output, {autoClose: true});
fileOut.write('Image,Confidence,Tag,Provider,Points\n');
for (const image of images) {
    const outputs = image[1];
    for (const key of Object.keys(outputs)) {
        const output = outputs[key];
        for (const tag of output) {
            fileOut.write(`${image[0]},${tag.confidence},${tag.tag},${key}\n`);
        }
    }
}
