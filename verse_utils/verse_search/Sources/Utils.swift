import Foundation

// Define a function that runs a shell command
func shell(command: String) -> String {
  let task = Process()
  let pipe = Pipe()

  task.standardOutput = pipe
  task.standardError = pipe
  task.arguments = ["-c", command]
  task.launchPath = "/bin/zsh"
  task.launch()

  let data = pipe.fileHandleForReading.readDataToEndOfFile()
  let output = String(data: data, encoding: .utf8)

  return output?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
}

func getBookFromArguments(arguments: Array<String>) throws -> (String, String) {
    let book: String
    let mappedBook: String
    let numericBook: Bool

    if arguments.count == 1 {
        //no specific book to search
        return ("*", "*")
    } else if let _ = Int(arguments[1]) {
        //the book starts with a number
        if arguments.count < 3 {
            throw VerseRequestorError.missingBookName
        }
        book = (arguments[1] + " " + arguments[2]).lowercased()
        numericBook = true
    } else {
        if arguments.count < 2 {
            throw VerseRequestorError.missingBookName
        }
        book = arguments[1].lowercased()
        numericBook = false
    }

    if let bookMap = books_map[book] {
        mappedBook = bookMap
    } else {
        throw VerseRequestorError.invalidBookName(book: book)
    }

    if numericBook {
        if arguments.count < 4 {
            return (mappedBook, "*")
        }

        if let _ = Int(arguments.last!) {
            return (mappedBook, arguments.last!)
        }

        throw VerseRequestorError.invalidChapterNumber(chapter: arguments.last!)
    } else {
        if arguments.count < 3 {
            return (mappedBook, "*")
        }

        if let _ = Int(arguments.last!) {
            return (mappedBook, arguments.last!)
        }
        throw VerseRequestorError.invalidChapterNumber(chapter: arguments.last!)
    }
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