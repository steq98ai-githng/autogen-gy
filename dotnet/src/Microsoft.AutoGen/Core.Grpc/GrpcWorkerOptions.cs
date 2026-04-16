// Copyright (c) Microsoft Corporation. All rights reserved.
// GrpcWorkerOptions.cs

using System.Threading.Channels;

namespace Microsoft.AutoGen.Core.Grpc;

public class GrpcWorkerOptions
{
    public BoundedChannelOptions ChannelOptions { get; set; } = new BoundedChannelOptions(1024)
    {
        AllowSynchronousContinuations = true,
        SingleReader = true,
        SingleWriter = false,
        FullMode = BoundedChannelFullMode.Wait
    };
}
