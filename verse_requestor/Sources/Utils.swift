import Foundation

func formatNewLine(content: String) -> String {
    return "🔻 " + content + "\n"
}

func isRangeOfVerses(arguments: Array<String>) -> Bool {
    let joinedargs = arguments[1...].joined(separator: " ") //Remove first input in case it is for a book that starts with a number.
    let expr = #"\d+"#

    if let regex = try? NSRegularExpression(pattern: expr) {
        let matches = regex.matches(in: joinedargs, range: NSRange(joinedargs.startIndex..., in: joinedargs))
        let matchStrings = matches.map { match in
            String(joinedargs[Range(match.range, in: joinedargs)!])
        }
        //if it is an entire chapter
        if matchStrings.count == 1 {return true}
    }

    return joinedargs.contains("-")
}

@available(macOS 13.0, *)
func isRangeOfVersesWithinChapter(arguments: String) throws -> Bool {
    let regex: Regex = try Regex("^.*\\s\\d+:\\d+-\\d+[^:]*$")
    if let _ = arguments.firstMatch(of: regex) {
        return true
    }
    return false
}

@available(macOS 13.0, *)
func isEntireChapter(arguments: String) throws -> Bool {
    let regex: Regex = try Regex("^.*\\s\\d+[^:]*$")
    if let _ = arguments.firstMatch(of: regex) {
        return true
    }
    return false
}

@available(macOS 13.0, *)
func isRangeOfVersesMultipleChapters(arguments: String) throws -> Bool {
    let regex: Regex = try Regex("^.*\\s\\d+:\\d+-\\d+:\\d+.*$")
    if let _ = arguments.firstMatch(of: regex) {
        return true
    }
    return false
}

func isListOfVerses(arguments: String) -> Bool {
    return arguments.contains(";")
}

func isSingleVerse(arguments: String) -> Bool {
    let count: Int = arguments.reduce(0) { $1 == ":" ? $0 + 1 : $0 }
    return count == 1 && !arguments.contains(";") && !arguments.contains("-") && !arguments.contains(".")
}

@available(macOS 13.0, *)
func isSingleFootnote(arguments: String) throws -> Bool {

    let regex: Regex = try Regex("[A-Za-z]+\\s+[0-9]+:[0-9]+\\.[0-9]+")
    if let _ = arguments.firstMatch(of: regex) {
        return true
    }
    return false
}

@available(macOS 13.0, *)
func isMultipleFootnotes(arguments: String) throws -> Bool {

    let regex: Regex = try Regex("[A-Za-z]+\\s+[0-9]+:[0-9]+\\.\\*")
    if let _ = arguments.firstMatch(of: regex) {
        return true
    }
    return false
}

func getBookFromArguments(arguments: Array<String>) throws -> String {
    let book: String
    if let _ = Int(arguments[0]) {
        //the book starts with a number
        if arguments.count < 2 {
            throw VerseRequestorError.missingBookName
        }
        book = arguments[0] + arguments[1]
    } else {
        if arguments.count < 1 {
            throw VerseRequestorError.missingBookName
        }
        book = arguments[0]
    }

    if let bookMap = books_map[book] {
        return bookMap
    } else {
        throw VerseRequestorError.invalidBookName(book: book)
    }
}

func getSingleReferenceFromArguments(arguments: Array<String>) throws -> (Int, Int) {
    let rawReference: String
    if let _ = Int(arguments[0]) {
        //the book starts with a number
        rawReference = arguments[2].trimmingCharacters(in: .whitespacesAndNewlines)
    } else {
        rawReference = arguments[1].trimmingCharacters(in: .whitespacesAndNewlines)
    }

    let splitRef = rawReference.split(separator: ":", maxSplits: 1)

    let chapter: Int
    if let ch = Int(splitRef[0]) {
        chapter = ch
    } else {
        throw VerseRequestorError.invalidChapterNumber(chapter: String(splitRef[0]))
    }

    let verse: Int
    if let ve = Int(splitRef[1]) {
        verse = ve
    } else {
        throw VerseRequestorError.invalidVerseNumber(verse: String(splitRef[1]))
    }

    return (chapter, verse)
}

@available(macOS 13.0, *)
func getRangeOfReferencesFromArguments(arguments: Array<String>) throws -> Array<Int> {

    //Improve this function later with regex named capture groups.
    let joinedargs = arguments[1...].joined(separator: " ") //Remove first input in case it is for a book that starts with a number.

    //let expr = #".*(?<ch>\d+).*(?<ve1>\d+)-(?<ve2>\d+).*"# for named capture groups
    let expr = #"\d+"#

    if let regex = try? NSRegularExpression(pattern: expr) {
        let matches = regex.matches(in: joinedargs, range: NSRange(joinedargs.startIndex..., in: joinedargs))
        let matchStrings = matches.map { match in
            String(joinedargs[Range(match.range, in: joinedargs)!])
        }

        var ret: [Int] = []
        for match in matchStrings {
            ret.append(Int(match)!)
        }
        return ret

    } else {
        throw VerseRequestorError.couldNotParseVerseRange(reference: joinedargs)
    }
}

func getVerseContent(verseDto: VerseDto) throws -> String {
    let combinedReference: String = verseDto.book + " " + String(verseDto.startingChapter) + ":" + String(verseDto.startingVerse)

    //print(FileManager.default.currentDirectoryPath)

    var url = basePath + "/Verses/\(verseDto.book)/\(verseDto.startingChapter)"

    // open the file for reading
    freopen(url, "r", stdin)
    // read the first verseNum - 1 lines and discard them
    for _ in 1..<verseDto.startingVerse {
        _ = readLine()
    }
    if verseDto.queryType == VerseQueryType.singleVerse {
        // read the verseNum line and print it
        if let line = readLine() {
            return line
        }
    } else if verseDto.queryType == VerseQueryType.verseRangeSingleChapter {
        let numMoreVerses = verseDto.endingVerse - verseDto.startingVerse
        var content: String = ""
        for _ in 0...numMoreVerses {
            if let line = readLine() {
                content += formatNewLine(content: line)
            }
        }
        if !content.isEmpty {return content}
    } else if verseDto.queryType == VerseQueryType.entireChapter {
        var content: String = ""
        while true {
            if let line = readLine() {
                content += formatNewLine(content: line)
            } else {
                break
            }
        }
        if !content.isEmpty {return content}
    } else if verseDto.queryType == VerseQueryType.verseRangeMultiChapter {
        var content: String = ""
        while true {
            if let line = readLine() {
                content += formatNewLine(content: line)
            } else {
                break
            }
        }

        let numMoreChapters = verseDto.endingChapter - verseDto.startingChapter
        for i in 1...numMoreChapters {
            url = basePath + "/Verses/\(verseDto.book)/\(verseDto.startingChapter + i)"
            freopen(url, "r", stdin)
            if i != numMoreChapters {
                while true {
                    if let line = readLine() {
                        content += formatNewLine(content: line)
                    } else {
                        break
                    }
                }
            } else {
                //on the last chapter
                for _ in 1...verseDto.endingVerse {
                    if let line = readLine() {
                        content += formatNewLine(content: line)
                    }
                }
            }
        }
        if !content.isEmpty {return content.trimmingCharacters(in: .whitespacesAndNewlines)}
    }
    
    throw VerseRequestorError.verseDoesNotExist(reference: combinedReference)
}

func getFootnoteContent(verseDto: VerseDto) throws -> String {
    if verseDto.queryType == VerseQueryType.singleFootnote {
        //one footnote
        let url = basePath + "/Footnotes/\(verseDto.book)/\(verseDto.startingChapter)/\(verseDto.startingVerse)/\(verseDto.footnote)"
        freopen(url, "r", stdin)
        
        if let line = readLine() {
            return line
        }
    } else if verseDto.queryType == VerseQueryType.allFootnotes {
        //all footnotes from verse

        let baseUrl = basePath + "/Footnotes/\(verseDto.book)/\(verseDto.startingChapter)/\(verseDto.startingVerse)/"
        var fnCounter = 1
        var url = baseUrl + String(fnCounter)

        var content: String = ""

        while FileManager.default.fileExists(atPath: url) {
            freopen(url, "r", stdin)

            if let line = readLine() {
                content += formatNewLine(content: line)
            }
            fnCounter += 1
            url = baseUrl + String(fnCounter)
        }
        return content.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    throw VerseRequestorError.noFootnoteSpecified(reference: "")
}

struct VerseDto {
    var book: String
    var startingChapter: Int
    var endingChapter: Int
    var startingVerse: Int
    var endingVerse: Int
    var footnote: Int
    var queryType: VerseQueryType
    var content: String
}

enum VerseQueryType {
    case singleVerse
    case verseRangeSingleChapter
    case verseRangeMultiChapter
    case entireChapter
    case singleFootnote
    case allFootnotes
    case undefined
}

enum VerseRequestorError: Error {
    case missingBookName
    case missingChapterNumber
    case missingVerseNumber
    case invalidVerseNumber(verse: String)
    case invalidChapterNumber(chapter: String)
    case invalidBookName(book: String)
    case couldNotRetrieveVerse(reference: String)
    case verseDoesNotExist(reference: String)
    case couldNotParseVerseRange(reference: String)
    case noFootnoteSpecified(reference: String)
}

let books_map: [String: String] = [
    "genesis": "Gen",
    "gn": "Gen",
    "exodus": "Exo",
    "ex": "Exo",
    "leviticus": "Lev",
    "lv": "Lev",
    "numbers": "Num",
    "deuteronomy": "Deut",
    "dt": "Deut",
    "joshua": "Josh",
    "judges": "Judg",
    "1 samuel": "1Sam",
    "1 sam": "1Sam",
    "2 samuel": "2Sam",
    "2 sam": "2Sam",
    "1 kings": "1Kings",
    "2 kings": "2Kings",
    "1 chronicles": "1Chron",
    "1 chron": "1Chron",
    "2 chronicles": "2Chron",
    "2 chron": "2Chron",
    "ez": "Ezra",
    "nehemiah": "Neh",
    "esth": "Esther",
    "es": "Esther",
    "est": "Esther",
    "jb": "Job",
    "psalm": "Psa",
    "psalms": "Psa",
    "ps": "Psa",
    "proverbs": "Prov",
    "prv": "Prov",
    "ecclesiastes": "Eccl",
    "ecc": "Eccl",
    "song of songs": "SOS",
    "song of solomon": "SOS",
    "isaiah": "Isa",
    "is": "Isa",
    "jeremiah": "Jer",
    "lamentations": "Lam",
    "ezekiel": "Ezek",
    "daniel": "Dan",
    "dn": "Dan",
    "hosea": "Hos",
    "obadiah": "Obad",
    "mic": "Micah",
    "nah": "Nahum",
    "habakkuk": "Hab",
    "zephaniah": "Zeph",
    "haggai": "Hag",
    "zechariah": "Zech",
    "malachi": "Mal",
    "matthew": "Matt",
    "mt": "Matt",
    "mk": "Mark",
    "luk": "Luke",
    "jn": "John",
    "ac": "Acts",
    "romans": "Rom",
    "rm": "Rom",
    "1 corinthians": "1Cor",
    "1 cor": "1Cor",
    "2 corinthians": "2Cor",
    "2 cor": "2Cor",
    "galatians": "Gal",
    "ephesians": "Eph",
    "philippians": "Phil",
    "colossians": "Col",
    "1 thessalonians": "1Thes",
    "1 thes": "1Thes",
    "2 thessalonians": "2Thes",
    "2 thes": "2Thes",
    "1 timothy": "1Tim",
    "1 tim": "1Tim",
    "2 timothy": "2Tim",
    "2 tim": "2Tim",
    "tit": "Titus",
    "tt": "Titus",
    "phm": "Philemon",
    "philem": "Philemon",
    "hebrews": "Heb",
    "jam": "James",
    "1 peter": "1Pet",
    "1 pet": "1Pet",
    "2 peter": "2Pet",
    "2 pet": "2Pet",
    "1 john": "1John",
    "1 jn": "1John",
    "2 john": "2John",
    "2 jn": "2John",
    "3 john": "3John",
    "3 jn": "3John",
    "jude": "Jude",
    "jud": "Jude",
    "revelation": "Rev",
    "rv": "Rev",
    "gen": "Gen",
    "exo": "Exo",
    "lev": "Lev",
    "num": "Num",
    "deut": "Deut",
    "josh": "Josh",
    "judg": "Judg",
    "ruth": "Ruth",
    "1sam": "1Sam",
    "2sam": "2Sam",
    "1kings": "1Kings",
    "2kings": "2Kings",
    "1chron": "1Chron",
    "2chron": "2Chron",
    "ezra": "Ezra",
    "neh": "Neh",
    "esther": "Esther",
    "job": "Job",
    "psa": "Psa",
    "prov": "Prov",
    "eccl": "Eccl",
    "sos": "SOS",
    "isa": "Isa",
    "jer": "Jer",
    "lam": "Lam",
    "ezek": "Ezek",
    "dan": "Dan",
    "hos": "Hos",
    "joel": "Joel",
    "amos": "Amos",
    "obad": "Obad",
    "jonah": "Jonah",
    "micah": "Micah",
    "nahum": "Nahum",
    "hab": "Hab",
    "zeph": "Zeph",
    "hag": "Hag",
    "zech": "Zech",
    "mal": "Mal",
    "matt": "Matt",
    "mark": "Mark",
    "luke": "Luke",
    "john": "John",
    "acts": "Acts",
    "rom": "Rom",
    "1cor": "1Cor",
    "2cor": "2Cor",
    "gal": "Gal",
    "eph": "Eph",
    "phil": "Phil",
    "col": "Col",
    "1thes": "1Thes",
    "2thes": "2Thes",
    "1tim": "1Tim",
    "2tim": "2Tim",
    "titus": "Titus",
    "philemon": "Philemon",
    "heb": "Heb",
    "james": "James",
    "1pet": "1Pet",
    "2pet": "2Pet",
    "1john": "1John",
    "2john": "2John",
    "3john": "3John",
    "rev": "Rev"
]