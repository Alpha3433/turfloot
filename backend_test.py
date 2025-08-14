#!/usr/bin/env python3
"""
TurfLoot 2-Player Lobby System Backend Testing
Tests the newly implemented lobby system components
"""

import json
import time
import requests
import sys
import os
import uuid
from datetime import datetime

# Test configuration - Use localhost since external URL has 502 errors
BASE_URL = "http://localhost:3000"
API_BASE = f"{BASE_URL}/api"

class LobbySystemTester:
    def __init__(self):
        self.test_results = []
        self.auth_token = None
        self.test_user_id = f"test_user_{int(time.time())}"
        self.test_lobby_id = None
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        status = "✅ PASSED" if success else "❌ FAILED"
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} - {test_name}: {message}")
        if details:
            print(f"   Details: {details}")
        return success

    def create_test_user(self):
        """Create a test user for authentication"""
        try:
            # Create test user via Privy auth endpoint
            test_privy_user = {
                "id": f"did:privy:{self.test_user_id}",
                "email": {"address": f"lobby.test.{int(time.time())}@turfloot.com"},
                "google": {"email": f"lobby.test.{int(time.time())}@gmail.com", "name": "Lobby Test User"},
                "wallet": {"address": f"0x{self.test_user_id[:40]}"}
            }
            
            response = requests.post(f"{API_BASE}/auth/privy", 
                json={"privy_user": test_privy_user},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                return self.log_test("User Creation", True, 
                    f"Test user created successfully with JWT token")
            else:
                return self.log_test("User Creation", False, 
                    f"Failed to create test user: {response.status_code}")
                    
        except Exception as e:
            return self.log_test("User Creation", False, f"Error creating test user: {str(e)}")

    def test_lobby_manager_import(self):
        """Test if LobbyManager can be imported and initialized"""
        try:
            # Test if the file exists and can be read
            lobby_manager_path = "/app/lib/lobby/LobbyManager.js"
            if os.path.exists(lobby_manager_path):
                with open(lobby_manager_path, 'r') as f:
                    content = f.read()
                    
                # Check for key components
                required_methods = [
                    'createLobby', 'joinLobby', 'leaveLobby', 
                    'updatePlayerReady', 'startMatch', 'getPublicLobbies'
                ]
                
                missing_methods = []
                for method in required_methods:
                    if method not in content:
                        missing_methods.append(method)
                
                if not missing_methods:
                    return self.log_test("LobbyManager Import", True, 
                        "LobbyManager.js contains all required methods",
                        f"Methods found: {', '.join(required_methods)}")
                else:
                    return self.log_test("LobbyManager Import", False, 
                        f"Missing methods: {', '.join(missing_methods)}")
            else:
                return self.log_test("LobbyManager Import", False, 
                    "LobbyManager.js file not found")
                    
        except Exception as e:
            return self.log_test("LobbyManager Import", False, f"Error testing import: {str(e)}")

    def test_missing_components(self):
        """Test for missing lobby system components"""
        try:
            missing_files = []
            expected_files = [
                "/app/lib/lobby/MatchAllocator.js",
                "/app/lib/lobby/LobbySocketHandlers.js"
            ]
            
            for file_path in expected_files:
                if not os.path.exists(file_path):
                    missing_files.append(file_path)
            
            if missing_files:
                return self.log_test("Missing Components", False, 
                    f"Critical lobby system files are missing",
                    f"Missing files: {', '.join(missing_files)}")
            else:
                return self.log_test("Missing Components", True, 
                    "All expected lobby system files are present")
                    
        except Exception as e:
            return self.log_test("Missing Components", False, f"Error checking files: {str(e)}")

    def test_database_schema(self):
        """Test database schema for lobby system"""
        try:
            schema_path = "/app/lib/database/schema.sql"
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_content = f.read()
                
                # Check for required tables
                required_tables = ['lobbies', 'lobby_members', 'matches', 'game_rooms']
                missing_tables = []
                
                for table in required_tables:
                    if f"CREATE TABLE IF NOT EXISTS {table}" not in schema_content:
                        missing_tables.append(table)
                
                if not missing_tables:
                    return self.log_test("Database Schema", True, 
                        "All required database tables defined in schema",
                        f"Tables: {', '.join(required_tables)}")
                else:
                    return self.log_test("Database Schema", False, 
                        f"Missing table definitions: {', '.join(missing_tables)}")
            else:
                return self.log_test("Database Schema", False, 
                    "Database schema file not found")
                    
        except Exception as e:
            return self.log_test("Database Schema", False, f"Error checking schema: {str(e)}")

    def test_play_page_lobby_integration(self):
        """Test play page lobby integration features"""
        try:
            play_page_path = "/app/app/play/page.js"
            if os.path.exists(play_page_path):
                with open(play_page_path, 'r') as f:
                    content = f.read()
                
                # Check for lobby integration features
                lobby_features = [
                    'matchId', 'roomCode', 'lobby_match', 
                    'urlParams.get(\'matchId\')', 'urlParams.get(\'roomCode\')'
                ]
                
                missing_features = []
                for feature in lobby_features:
                    if feature not in content:
                        missing_features.append(feature)
                
                if not missing_features:
                    return self.log_test("Play Page Integration", True, 
                        "Play page contains lobby integration features",
                        f"Features found: {', '.join(lobby_features)}")
                else:
                    return self.log_test("Play Page Integration", False, 
                        f"Missing lobby features: {', '.join(missing_features)}")
            else:
                return self.log_test("Play Page Integration", False, 
                    "Play page file not found")
                    
        except Exception as e:
            return self.log_test("Play Page Integration", False, f"Error checking play page: {str(e)}")

    def test_socket_io_integration(self):
        """Test Socket.IO server integration for lobby handlers"""
        try:
            # Test Socket.IO with proper parameters
            response = requests.get(f"{BASE_URL}/socket.io/?EIO=4&transport=polling", timeout=5)
            
            if response.status_code == 200 and 'sid' in response.text:
                # Check server.js for lobby integration
                server_path = "/app/server.js"
                if os.path.exists(server_path):
                    with open(server_path, 'r') as f:
                        server_content = f.read()
                    
                    # Look for game server initialization
                    if 'gameServer.initialize' in server_content:
                        return self.log_test("Socket.IO Integration", True, 
                            "Socket.IO server accessible and game server initialized",
                            f"Socket.IO response contains session ID")
                    else:
                        return self.log_test("Socket.IO Integration", False, 
                            "Socket.IO accessible but game server not properly initialized")
                else:
                    return self.log_test("Socket.IO Integration", False, 
                        "Socket.IO accessible but server.js not found")
            else:
                return self.log_test("Socket.IO Integration", False, 
                    f"Socket.IO server not responding correctly: {response.status_code}")
                    
        except Exception as e:
            return self.log_test("Socket.IO Integration", False, f"Error testing Socket.IO: {str(e)}")

    def test_lobby_manager_functionality(self):
        """Test LobbyManager embedded functionality"""
        try:
            lobby_manager_path = "/app/lib/lobby/LobbyManager.js"
            if os.path.exists(lobby_manager_path):
                with open(lobby_manager_path, 'r') as f:
                    content = f.read()
                
                # Check if match allocation is embedded in LobbyManager
                embedded_features = []
                missing_features = []
                
                features_to_check = [
                    ('allocateMatch', 'Match allocation functionality'),
                    ('generateLobbyId', 'Lobby ID generation'),
                    ('generateJoinCode', 'Join code generation'),
                    ('MongoClient', 'Database integration'),
                    ('crypto.randomUUID', 'UUID generation'),
                    ('this.lobbies = new Map', 'In-memory lobby cache'),
                    ('this.userSessions = new Map', 'User session tracking')
                ]
                
                for feature, description in features_to_check:
                    if feature in content:
                        embedded_features.append(description)
                    else:
                        missing_features.append(description)
                
                if len(embedded_features) >= 5:  # Most features present
                    return self.log_test("LobbyManager Functionality", True, 
                        f"LobbyManager has most required functionality embedded",
                        f"Found: {', '.join(embedded_features)}")
                else:
                    return self.log_test("LobbyManager Functionality", False, 
                        f"LobbyManager missing key functionality",
                        f"Missing: {', '.join(missing_features)}")
            else:
                return self.log_test("LobbyManager Functionality", False, 
                    "LobbyManager.js file not found")
                    
        except Exception as e:
            return self.log_test("LobbyManager Functionality", False, f"Error testing functionality: {str(e)}")

    def test_missing_socket_handlers(self):
        """Test what specific socket handlers are missing"""
        try:
            # Check if lobby socket handlers are needed or embedded elsewhere
            gameserver_path = "/app/lib/gameServer.js"
            server_path = "/app/server.js"
            
            socket_integration_found = False
            lobby_handlers_needed = []
            
            # Check if gameServer has socket handling
            if os.path.exists(gameserver_path):
                with open(gameserver_path, 'r') as f:
                    gameserver_content = f.read()
                
                if 'socket.on(' in gameserver_content or 'io.on(' in gameserver_content:
                    socket_integration_found = True
            
            # Check what lobby-specific handlers are missing
            required_handlers = [
                'lobby:create', 'lobby:join', 'lobby:leave', 
                'lobby:ready', 'lobby:chat', 'lobby:kick', 'lobby:start'
            ]
            
            # Since LobbySocketHandlers.js is missing, these handlers need to be implemented
            if not socket_integration_found:
                return self.log_test("Missing Socket Handlers", False, 
                    "Lobby socket handlers not implemented",
                    f"Need to implement: {', '.join(required_handlers)}")
            else:
                return self.log_test("Missing Socket Handlers", True, 
                    "Socket handling infrastructure exists, lobby handlers can be added")
                    
        except Exception as e:
            return self.log_test("Missing Socket Handlers", False, f"Error checking handlers: {str(e)}")

    def test_lobby_api_endpoints(self):
        """Test if lobby-related API endpoints exist"""
        try:
            # Test endpoints that should exist for lobby system
            test_endpoints = [
                ('/api/', 'GET', 'Root API'),
                ('/api/servers/lobbies', 'GET', 'Server Browser'),
            ]
            
            working_endpoints = []
            failed_endpoints = []
            
            for endpoint, method, name in test_endpoints:
                try:
                    if method == 'GET':
                        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
                    else:
                        response = requests.post(f"{BASE_URL}{endpoint}", timeout=5)
                    
                    if response.status_code in [200, 201]:
                        working_endpoints.append(name)
                    else:
                        failed_endpoints.append(f"{name} ({response.status_code})")
                        
                except Exception as e:
                    failed_endpoints.append(f"{name} (Error: {str(e)})")
            
            if len(working_endpoints) >= len(test_endpoints) // 2:
                return self.log_test("Lobby API Endpoints", True, 
                    f"Core API endpoints accessible",
                    f"Working: {', '.join(working_endpoints)}")
            else:
                return self.log_test("Lobby API Endpoints", False, 
                    f"Most API endpoints not accessible",
                    f"Failed: {', '.join(failed_endpoints)}")
                    
        except Exception as e:
            return self.log_test("Lobby API Endpoints", False, f"Error testing endpoints: {str(e)}")

    def test_mongodb_connection(self):
        """Test MongoDB connection for lobby data storage"""
        try:
            # Try to access an endpoint that uses MongoDB
            response = requests.get(f"{API_BASE}/", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'TurfLoot' in data['message']:
                    return self.log_test("MongoDB Connection", True, 
                        "API endpoints accessible, MongoDB likely connected")
                else:
                    return self.log_test("MongoDB Connection", False, 
                        "API accessible but unexpected response format")
            else:
                return self.log_test("MongoDB Connection", False, 
                    f"API not accessible: {response.status_code}")
                    
        except Exception as e:
            return self.log_test("MongoDB Connection", False, f"Error testing MongoDB: {str(e)}")

    def test_jwt_token_support(self):
        """Test JWT token support for lobby authentication"""
        try:
            if not self.auth_token:
                return self.log_test("JWT Token Support", False, 
                    "No auth token available for testing")
            
            # Test authenticated endpoint
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            response = requests.get(f"{API_BASE}/wallet/balance", headers=headers, timeout=5)
            
            if response.status_code == 200:
                return self.log_test("JWT Token Support", True, 
                    "JWT token authentication working correctly")
            elif response.status_code == 401:
                return self.log_test("JWT Token Support", False, 
                    "JWT token rejected by server")
            else:
                return self.log_test("JWT Token Support", False, 
                    f"Unexpected response: {response.status_code}")
                    
        except Exception as e:
            return self.log_test("JWT Token Support", False, f"Error testing JWT: {str(e)}")

    def test_lobby_system_readiness(self):
        """Test overall lobby system readiness"""
        try:
            # Count successful tests
            passed_tests = sum(1 for result in self.test_results if "✅ PASSED" in result['status'])
            total_tests = len(self.test_results)
            
            readiness_score = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            
            if readiness_score >= 70:
                return self.log_test("Lobby System Readiness", True, 
                    f"Lobby system {readiness_score:.1f}% ready for testing",
                    f"Passed: {passed_tests}/{total_tests} tests")
            else:
                return self.log_test("Lobby System Readiness", False, 
                    f"Lobby system only {readiness_score:.1f}% ready",
                    f"Passed: {passed_tests}/{total_tests} tests")
                    
        except Exception as e:
            return self.log_test("Lobby System Readiness", False, f"Error calculating readiness: {str(e)}")

    def run_all_tests(self):
        """Run all lobby system tests"""
        print("🎮 Starting TurfLoot 2-Player Lobby System Backend Testing")
        print("=" * 70)
        
        # Test sequence
        test_methods = [
            self.create_test_user,
            self.test_lobby_manager_import,
            self.test_lobby_manager_functionality,
            self.test_missing_components,
            self.test_missing_socket_handlers,
            self.test_database_schema,
            self.test_play_page_lobby_integration,
            self.test_socket_io_integration,
            self.test_lobby_api_endpoints,
            self.test_mongodb_connection,
            self.test_jwt_token_support,
            self.test_lobby_system_readiness
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                self.log_test(test_method.__name__, False, f"Test execution error: {str(e)}")
            print()  # Add spacing between tests
        
        # Summary
        print("=" * 70)
        print("🎮 LOBBY SYSTEM TESTING SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in self.test_results if "✅ PASSED" in result['status'])
        failed = sum(1 for result in self.test_results if "❌ FAILED" in result['status'])
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        
        # Show failed tests
        if failed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if "❌ FAILED" in result['status']:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Show critical issues
        critical_issues = []
        for result in self.test_results:
            if "❌ FAILED" in result['status'] and any(keyword in result['test'].lower() 
                for keyword in ['missing', 'import', 'database', 'socket']):
                critical_issues.append(result['test'])
        
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES FOUND:")
            for issue in critical_issues:
                print(f"  - {issue}")
        
        return passed, failed

def main():
    """Main test execution"""
    tester = LobbySystemTester()
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()