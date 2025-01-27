import Foundation
var basePath = Bundle.main.bundlePath

#if DEBUG
print("Debug mode")
basePath = FileManager.default.currentDirectoryPath
#endif

let terminalArguments: Array<String> = Array(CommandLine.arguments.dropFirst()) // There is always one argument passed, which is the name of the program, we get rid of it here.
if terminalArguments.isEmpty {
    print("No arguments passed")
    exit(EXIT_FAILURE)
}
let joinedArguments: String = terminalArguments.joined(separator: " ").trimmingCharacters(in: .whitespacesAndNewlines)

var verseData = VerseDto(
    book: "",
    startingChapter: 0,
    endingChapter: 0,
    startingVerse: 0,
    endingVerse: 0,
    footnote: 0,
    queryType: VerseQueryType.undefined,
    content: ""
)

if #available(macOS 13.0, *) {
    do {
        verseData.book = try getBookFromArguments(arguments: terminalArguments)

        if isRangeOfVerses(arguments: terminalArguments) {
            if try isEntireChapter(arguments: joinedArguments) {
                //print("Entire chapter")
                let chV1V2: [Int] = try getRangeOfReferencesFromArguments(arguments: terminalArguments)
                verseData.startingChapter = chV1V2[0]
                verseData.startingVerse = 1
                verseData.queryType = VerseQueryType.entireChapter

                verseData.content = try getVerseContent(verseDto: verseData)

            }

            if try isRangeOfVersesWithinChapter(arguments: joinedArguments) {
                //print("Range of verses within a chapter: true")
                let chV1V2: [Int] = try getRangeOfReferencesFromArguments(arguments: terminalArguments)
                verseData.startingChapter = chV1V2[0]
                verseData.endingChapter = chV1V2[0]
                verseData.startingVerse = chV1V2[1]
                verseData.endingVerse = chV1V2[2]
                verseData.queryType = VerseQueryType.verseRangeSingleChapter

                verseData.content = try getVerseContent(verseDto: verseData)
            }

            if try isRangeOfVersesMultipleChapters(arguments: joinedArguments) {
                //print("Range of verses multiple chapters: true")
                let chV1V2: [Int] = try getRangeOfReferencesFromArguments(arguments: terminalArguments)
                verseData.startingChapter = chV1V2[0]
                verseData.endingChapter = chV1V2[2]
                verseData.startingVerse = chV1V2[1]
                verseData.endingVerse = chV1V2[3]
                verseData.queryType = VerseQueryType.verseRangeMultiChapter

                verseData.content = try getVerseContent(verseDto: verseData)
            }


        } else if isListOfVerses(arguments: joinedArguments) {
            print("List of verses not yet supported")
        } else if isSingleVerse(arguments: joinedArguments) {
            let reference: (Int, Int) = try getSingleReferenceFromArguments(arguments: terminalArguments)
            verseData.startingChapter = reference.0
            verseData.startingVerse = reference.1
            verseData.queryType = VerseQueryType.singleVerse

            verseData.content = try getVerseContent(verseDto: verseData)
        } else if try isSingleFootnote(arguments: joinedArguments) {
            //print("single footnote")
            let chVFn: [Int] = try getRangeOfReferencesFromArguments(arguments: terminalArguments)
            verseData.queryType = VerseQueryType.singleFootnote
            verseData.startingChapter = chVFn[0]
            verseData.startingVerse = chVFn[1]
            verseData.footnote = chVFn[2]

            verseData.content = try getFootnoteContent(verseDto: verseData)
        } else if try isMultipleFootnotes(arguments: joinedArguments) {
            //print("multiple footnotes")
            let chVFn: [Int] = try getRangeOfReferencesFromArguments(arguments: terminalArguments)
            verseData.queryType = VerseQueryType.allFootnotes
            verseData.startingChapter = chVFn[0]
            verseData.startingVerse = chVFn[1]

            verseData.content = try getFootnoteContent(verseDto: verseData)
        }
        
    } catch let errorType {
        print("There was a problem with your query: \(errorType)")
        exit(EXIT_FAILURE)
    }
} else {
    print("Only MacOS 13.0+ is supported")
    exit(EXIT_SUCCESS)
}

if verseData.content.isEmpty{
    print("There was an unhandled error with your query")
} else {
    print(verseData.content)
}