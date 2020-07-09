
import XCTest
import Firebase

class Wifi_testUITests: XCTestCase {
    
    let app = XCUIApplication()
    let hours = 10
    
    
    override func setUp() {
        super.setUp()
        continueAfterFailure = true
        app.launch()
    }

    override func tearDown() {
        app.terminate()
    }

    func testTimer_ALEOS() {
        var index = 0
        let cellQuery = self.app.tables.cells.element(boundBy: index)
        cellQuery.buttons["Connect"].tap()
        let systemAlerts = XCUIApplication(bundleIdentifier: "com.apple.springboard").alerts
        while true{
            if systemAlerts.buttons["Join"].exists {
                systemAlerts.buttons["Join"].tap()
                app.tap()
            }
            if systemAlerts.buttons["OK"].exists {
                systemAlerts.buttons["OK"].tap()
                app.tap()
            }
            if index >= 3600*self.hours{break}
            index += 1
            sleep(1)
        }
    }

    func testTimer_MGOS() {
        
        app.segmentedControls.buttons["MGOS"].tap()
        
        var index = 0
        let cellQuery = self.app.tables.cells.element(boundBy: index)
        cellQuery.buttons["Connect"].tap()
        let systemAlerts = XCUIApplication(bundleIdentifier: "com.apple.springboard").alerts
        while true{
            if systemAlerts.buttons["Join"].exists {
                systemAlerts.buttons["Join"].tap()
                app.tap()
            }
            if systemAlerts.buttons["OK"].exists {
                systemAlerts.buttons["OK"].tap()
                app.tap()
            }
            if index >= 3600*self.hours{break}
            index += 1
            sleep(1)
        }
    }
    
    
}
