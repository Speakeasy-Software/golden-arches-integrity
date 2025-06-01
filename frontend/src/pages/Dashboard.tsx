import React from 'react';
import { useQuery } from 'react-query';
import {
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Clock,
  Upload as UploadIcon,
  Image,
  BarChart3,
} from 'lucide-react';
import { dashboardApi } from '@/services/api';
import { formatPercentage } from '@/utils';

interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon: React.ElementType;
  color: 'green' | 'red' | 'yellow' | 'blue';
}

function StatCard({ title, value, change, icon: Icon, color }: StatCardProps) {
  const colorClasses = {
    green: 'bg-green-100 text-green-600',
    red: 'bg-red-100 text-red-600',
    yellow: 'bg-yellow-100 text-yellow-600',
    blue: 'bg-blue-100 text-blue-600',
  };

  return (
    <div className="card">
      <div className="card-content">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className="text-2xl font-bold text-gray-900">{value}</p>
            {change !== undefined && (
              <div className="flex items-center mt-1">
                {change >= 0 ? (
                  <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                ) : (
                  <TrendingDown className="w-4 h-4 text-red-500 mr-1" />
                )}
                <span
                  className={`text-sm ${
                    change >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {Math.abs(change)}% from last month
                </span>
              </div>
            )}
          </div>
          <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
            <Icon className="w-6 h-6" />
          </div>
        </div>
      </div>
    </div>
  );
}

interface RecentActivityItem {
  id: string;
  type: 'upload' | 'analysis' | 'violation' | 'approval';
  message: string;
  timestamp: string;
  severity?: 'low' | 'medium' | 'high' | 'critical';
}

function RecentActivity() {
  // Mock data - in real app this would come from API
  const activities: RecentActivityItem[] = [
    {
      id: '1',
      type: 'violation',
      message: 'Critical violation detected in asset_12345.jpg - Logo rotation detected',
      timestamp: '2 minutes ago',
      severity: 'critical',
    },
    {
      id: '2',
      type: 'upload',
      message: '15 new assets uploaded for review',
      timestamp: '5 minutes ago',
    },
    {
      id: '3',
      type: 'approval',
      message: 'Asset batch_001 approved by Brand Team',
      timestamp: '10 minutes ago',
    },
    {
      id: '4',
      type: 'analysis',
      message: 'Batch analysis completed for 25 assets',
      timestamp: '15 minutes ago',
    },
    {
      id: '5',
      type: 'violation',
      message: 'Background legibility issue in heritage_logo_03.png',
      timestamp: '20 minutes ago',
      severity: 'medium',
    },
  ];

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'upload':
        return <UploadIcon className="w-4 h-4 text-blue-500" />;
      case 'analysis':
        return <BarChart3 className="w-4 h-4 text-purple-500" />;
      case 'violation':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'approval':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      default:
        return <Clock className="w-4 h-4 text-gray-500" />;
    }
  };

  const getSeverityColor = (severity?: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'high':
        return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low':
        return 'text-green-600 bg-green-50 border-green-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
      </div>
      <div className="card-content">
        <div className="space-y-4">
          {activities.map((activity) => (
            <div
              key={activity.id}
              className={`flex items-start space-x-3 p-3 rounded-lg border ${getSeverityColor(
                activity.severity
              )}`}
            >
              <div className="flex-shrink-0 mt-0.5">
                {getActivityIcon(activity.type)}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-900">{activity.message}</p>
                <p className="text-xs text-gray-500 mt-1">{activity.timestamp}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ComplianceOverview() {
  const { data: stats, isLoading } = useQuery('dashboard-stats', dashboardApi.getStats);

  if (isLoading || !stats) {
    return (
      <div className="card">
        <div className="card-content">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
            <div className="h-3 bg-gray-200 rounded w-1/3"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-medium text-gray-900">Compliance Overview</h3>
      </div>
      <div className="card-content">
        <div className="space-y-4">
          {/* Compliance Rate */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Overall Compliance Rate</span>
              <span className="text-sm font-bold text-gray-900">
                {formatPercentage(stats.compliance_rate / 100)}
              </span>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${stats.compliance_rate}%` }}
              ></div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{stats.compliant_assets}</p>
              <p className="text-xs text-gray-500">Compliant Assets</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-red-600">{stats.critical_violations}</p>
              <p className="text-xs text-gray-500">Critical Violations</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery('dashboard-stats', dashboardApi.getStats);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="card">
              <div className="card-content">
                <div className="animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                  <div className="h-8 bg-gray-200 rounded w-3/4"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-golden rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">Welcome to Golden Arches Integrity</h1>
        <p className="text-white/90">
          Monitor and maintain McDonald's brand compliance across all your digital assets.
        </p>
      </div>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Assets"
            value={stats.total_assets.toLocaleString()}
            change={12}
            icon={Image}
            color="blue"
          />
          <StatCard
            title="Compliance Rate"
            value={formatPercentage(stats.compliance_rate / 100)}
            change={5}
            icon={CheckCircle}
            color="green"
          />
          <StatCard
            title="Pending Review"
            value={stats.pending_review}
            change={-8}
            icon={Clock}
            color="yellow"
          />
          <StatCard
            title="Critical Issues"
            value={stats.critical_violations}
            change={-15}
            icon={AlertTriangle}
            color="red"
          />
        </div>
      )}

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <RecentActivity />
        </div>
        <div>
          <ComplianceOverview />
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="btn-primary flex items-center justify-center space-x-2">
              <UploadIcon className="w-4 h-4" />
              <span>Upload Assets</span>
            </button>
            <button className="btn-secondary flex items-center justify-center space-x-2">
              <BarChart3 className="w-4 h-4" />
              <span>Run Analysis</span>
            </button>
            <button className="btn-secondary flex items-center justify-center space-x-2">
              <CheckCircle className="w-4 h-4" />
              <span>Review Pending</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 