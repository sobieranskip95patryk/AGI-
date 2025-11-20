#!/usr/bin/env python3
"""
🚀 TSGC Phase 3.2 Test Runner

Quick test execution script dla TSGC Pipeline validation:
- Automated test discovery i execution
- Component availability checking
- Performance benchmarking
- Result reporting i analysis
- Integration z pytest framework

Usage:
  python run_tsgc_tests.py                    # Run all tests
  python run_tsgc_tests.py --unit             # Unit tests only  
  python run_tsgc_tests.py --integration      # Integration tests only
  python run_tsgc_tests.py --performance      # Performance tests only
  python run_tsgc_tests.py --quick            # Quick smoke tests
"""

import sys
import argparse
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tests.test_tsgc_framework import TSGCTestRunner

def check_dependencies():
    """
    Check if required dependencies are available
    """
    print("🔍 Checking dependencies...")
    
    dependencies = {
        'torch': False,
        'numpy': False,
        'pytest': False
    }
    
    try:
        import torch
        dependencies['torch'] = True
        print("✅ PyTorch available")
    except ImportError:
        print("❌ PyTorch not available")
    
    try:
        import numpy
        dependencies['numpy'] = True
        print("✅ NumPy available")
    except ImportError:
        print("❌ NumPy not available")
    
    try:
        import pytest
        dependencies['pytest'] = True
        print("✅ Pytest available")
    except ImportError:
        print("❌ Pytest not available")
    
    # Check TSGC components
    try:
        from TSGC import TransformerEncoder
        print("✅ TSGC TransformerEncoder available")
        dependencies['TSGC'] = True
    except ImportError:
        print("❌ TSGC components not available")
        dependencies['TSGC'] = False
    
    return dependencies

def run_quick_smoke_test():
    """
    Quick smoke test dla basic functionality
    """
    print("\n🚀 Running Quick Smoke Test...")
    
    try:
        # Test basic imports
        from tests.test_tsgc_framework import TSGCTestFixtures
        
        fixtures = TSGCTestFixtures()
        
        # Test fixture data
        sequences = fixtures.get_medical_sequences()
        tokens = fixtures.get_sample_tokens()
        config = fixtures.get_test_config()
        
        print(f"✅ Sample sequences: {len(sequences)} available")
        print(f"✅ Test tokens: {len(tokens)} available")
        print(f"✅ Test config: d_model={config['d_model']}")
        
        # Test mock node creation
        mock_node = fixtures.create_mock_symbolic_node("test_node")
        if mock_node:
            print(f"✅ Mock node creation successful")
        else:
            print("⚠️ Mock node creation requires TSGC")
        
        return True
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        return False

def run_unit_tests():
    """
    Run unit tests only
    """
    print("\n📋 Running Unit Tests...")
    
    runner = TSGCTestRunner("test_results/unit")
    unit_tests = runner.unit_tests
    
    results = [
        unit_tests.test_transformer_encoder(),
        unit_tests.test_graph_mapper(),
        unit_tests.test_edge_constructor()
    ]
    
    successful = sum(1 for r in results if r.success)
    print(f"📊 Unit Tests: {successful}/{len(results)} passed")
    
    return results

def run_integration_tests():
    """
    Run integration tests only
    """
    print("\n🔗 Running Integration Tests...")
    
    runner = TSGCTestRunner("test_results/integration")
    integration_tests = runner.integration_tests
    
    results = [
        integration_tests.test_fusion_interface_complete_pipeline(),
        integration_tests.test_ilp_integration()
    ]
    
    successful = sum(1 for r in results if r.success)
    print(f"📊 Integration Tests: {successful}/{len(results)} passed")
    
    return results

def run_performance_tests():
    """
    Run performance tests only
    """
    print("\n⚡ Running Performance Tests...")
    
    runner = TSGCTestRunner("test_results/performance")
    performance_tests = runner.performance_tests
    
    results = [
        performance_tests.test_latency_benchmark(),
        performance_tests.test_memory_usage()
    ]
    
    successful = sum(1 for r in results if r.success)
    print(f"📊 Performance Tests: {successful}/{len(results)} passed")
    
    return results

def run_comprehensive_tests():
    """
    Run complete test suite
    """
    print("\n🧪 Running Comprehensive Test Suite...")
    
    runner = TSGCTestRunner("test_results/comprehensive")
    summary = runner.run_all_tests()
    
    return summary

def main():
    """
    Main test runner entry point
    """
    parser = argparse.ArgumentParser(description="TSGC Phase 3.2 Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--quick", action="store_true", help="Run quick smoke test only")
    parser.add_argument("--check-deps", action="store_true", help="Check dependencies only")
    
    args = parser.parse_args()
    
    print("🧪 TSGC Phase 3.2 Test Runner")
    print("=" * 50)
    
    # Check dependencies first
    deps = check_dependencies()
    
    if args.check_deps:
        return
    
    # Run appropriate tests
    start_time = time.time()
    
    try:
        if args.quick:
            success = run_quick_smoke_test()
            if success:
                print("\n✅ Quick smoke test completed successfully")
            else:
                print("\n❌ Quick smoke test failed")
                return 1
                
        elif args.unit:
            results = run_unit_tests()
            successful = sum(1 for r in results if r.success)
            print(f"\n📊 Unit Tests Summary: {successful}/{len(results)} passed")
            
        elif args.integration:
            results = run_integration_tests()
            successful = sum(1 for r in results if r.success)
            print(f"\n📊 Integration Tests Summary: {successful}/{len(results)} passed")
            
        elif args.performance:
            results = run_performance_tests()
            successful = sum(1 for r in results if r.success)
            print(f"\n📊 Performance Tests Summary: {successful}/{len(results)} passed")
            
        else:
            # Run comprehensive tests
            summary = run_comprehensive_tests()
            
            print(f"\n🎯 Comprehensive Test Summary:")
            print(f"   Total Tests: {summary['total_tests']}")
            print(f"   Successful: {summary['successful_tests']}")
            print(f"   Success Rate: {summary['success_rate']:.1%}")
            print(f"   Average Confidence: {summary['average_confidence']:.3f}")
            
            if summary['success_rate'] >= 0.8:
                print("\n✅ TSGC Phase 3.2 validation SUCCESSFUL")
                return 0
            else:
                print("\n⚠️ TSGC Phase 3.2 validation needs attention")
                return 1
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        return 1
        
    finally:
        total_time = time.time() - start_time
        print(f"\n⏱️ Total execution time: {total_time:.2f}s")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)